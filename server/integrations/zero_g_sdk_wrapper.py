import subprocess
import json
import os
import tempfile
from typing import Optional


class ZeroGSDKWrapper:
    """
    Thin, deterministic wrapper around the 0G Go-based Python SDK.
    This isolates ALL Go complexity from the rest of the system.
    """

    def __init__(self, binary_path: Optional[str] = None):
        # If SDK builds a binary, we store path here
        self.binary_path = binary_path or os.getenv("ZOG_BINARY", "0g")

    # -------------------------
    # LOW LEVEL EXECUTION CORE
    # -------------------------

    def _run(self, args: list[str], input_data: bytes | None = None) -> str:
        try:
            result = subprocess.run(
                [self.binary_path] + args,
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            return result.stdout.decode("utf-8")

        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"0G SDK error: {e.stderr.decode('utf-8', errors='ignore')}"
            )

    # -------------------------
    # HIGH LEVEL OPERATIONS
    # -------------------------

    def upload_bytes(self, data: bytes, metadata: dict | None = None) -> str:
        """
        Upload raw bytes to 0G storage.
        Returns storage_id (CID / pointer).
        """

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(data)
            temp_path = f.name

        try:
            args = ["upload", temp_path]

            if metadata:
                args += ["--meta", json.dumps(metadata)]

            output = self._run(args)

            # Expect SDK returns JSON like: {"id": "..."}
            parsed = json.loads(output)
            return parsed["id"]

        finally:
            os.remove(temp_path)

    def download_bytes(self, storage_id: str) -> bytes:
        """
        Download raw bytes from 0G storage.
        """

        output = self._run(["download", storage_id])

        # SDK may return base64 or raw
        try:
            parsed = json.loads(output)
            if "data" in parsed:
                return parsed["data"].encode()
        except Exception:
            pass

        return output.encode()
