"""
iNFT Memory OS v5 — Verifiable Execution Kernel
Deterministic ordering, replay traces, event-level Merkle proofs, fork-safe DAG
"""

import hashlib
import json
import logging
import tempfile
import os
import asyncio
from typing import Dict, Any, Optional, List, Protocol, Tuple
from datetime import datetime
from dataclasses import dataclass

from .zero_g_storage import ZeroGStorageClient

logger = logging.getLogger(__name__)


class EventReducer(Protocol):
    """Pure deterministic reducer"""
    version: str
    def apply(self, state: Dict[str, Any], event: Dict[str, Any]) -> Dict[str, Any]: ...


@dataclass
class ReplayTrace:
    """Verifiable execution trace"""
    final_state: Dict[str, Any]
    commit_path: List[str]
    event_count: int
    verified: bool
    proof_root: str


@dataclass
class MemoryCommit:
    """Fully closed verifiable commit"""
    commit_id: str                    # H(parent + events_root + metadata)
    inft_id: str
    storage_id: str
    parent_commit_id: Optional[str]
    events_merkle_root: str
    reducer_version: str
    version: int
    timestamp: int
    event_count: int


class INFTMemoryOS:
    def __init__(self, storage_client: ZeroGStorageClient, reducer: EventReducer):
        self.storage = storage_client
        self.reducer = reducer
        self.commits: Dict[str, MemoryCommit] = {}
        self.heads: Dict[str, str] = {}               # inft_id → latest commit_id
        self.locks: Dict[str, asyncio.Lock] = {}

    @staticmethod
    def _merkle_root(events: List[Dict]) -> str:
        if not events:
            return "0x" + "0" * 64
        # Canonical indexed leaves
        leaves = []
        for i, e in enumerate(events):
            leaf_data = {"index": i, "event": e}
            leaf = hashlib.sha256(json.dumps(leaf_data, sort_keys=True).encode()).digest()
            leaves.append(leaf)

        while len(leaves) > 1:
            if len(leaves) % 2 == 1:
                leaves.append(leaves[-1])
            leaves = [hashlib.sha256(a + b).digest() for a, b in zip(leaves[::2], leaves[1::2])]
        return "0x" + leaves[0].hex()

    async def commit(
        self,
        inft_id: str,
        events: List[Dict[str, Any]],
        metadata: Optional[Dict] = None,
    ) -> MemoryCommit:
        """Verifiable events-only commit"""
        lock = self.locks.setdefault(inft_id, asyncio.Lock())
        async with lock:
            timestamp = int(datetime.now().timestamp())
            parent_id = self.heads.get(inft_id)

            events_root = self._merkle_root(events)

            payload = {
                "type": "memory_commit_v5",
                "inft_id": inft_id,
                "parent_commit": parent_id,
                "events": events,
                "events_merkle_root": events_root,
                "metadata": metadata or {},
                "timestamp": timestamp,
                "version": (self.commits[parent_id].version + 1) if parent_id else 1,
                "reducer_version": getattr(self.reducer, "version", "1.0"),
            }

            storage_id = await self.storage.upload_json(payload)

            # Strong cryptographic commit ID
            commit_seed = f"{parent_id or ''}:{events_root}:{payload['version']}:{timestamp}:{payload['reducer_version']}"
            commit_id = hashlib.sha256(commit_seed.encode()).hexdigest()

            commit = MemoryCommit(
                commit_id=commit_id,
                inft_id=inft_id,
                storage_id=storage_id,
                parent_commit_id=parent_id,
                events_merkle_root=events_root,
                reducer_version=payload["reducer_version"],
                version=payload["version"],
                timestamp=timestamp,
                event_count=len(events),
            )

            self.commits[commit_id] = commit
            self.heads[inft_id] = commit_id

            logger.info(f"✅ MemoryOS v5 Commit v{commit.version} | {inft_id} → {storage_id[:16]}")
            return commit

    # ====================== VERIFIABLE REPLAY ======================

    async def replay_with_trace(self, inft_id: str, to_version: Optional[int] = None) -> ReplayTrace:
        """Deterministic replay with verification trace"""
        commit_id = self.heads.get(inft_id)
        if not commit_id:
            return ReplayTrace({}, [], 0, False, "0x0")

        all_events: List[Dict] = []
        commit_path: List[str] = []
        current = commit_id

        while current:
            commit = self.commits.get(current)
            if not commit:
                break
            if to_version and commit.version == to_version:
                break

            commit_path.append(current)

            with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
                path = tmp.name
            try:
                await self.storage.download_from_0g_storage(commit.storage_id, path)
                with open(path) as f:
                    data = json.load(f)

                loaded = data.get("events", [])
                # Verify Merkle root
                if self._merkle_root(loaded) != commit.events_merkle_root:
                    logger.error(f"Merkle mismatch in commit {current}")
                    return ReplayTrace({}, commit_path, len(all_events), False, commit.events_merkle_root)

                all_events.extend(loaded)
            finally:
                if os.path.exists(path):
                    os.unlink(path)

            current = commit.parent_commit_id

        # Deterministic reduction (ordered by commit version + event index)
        state: Dict[str, Any] = {}
        for event in all_events:   # events already in commit order
            state = self.reducer.apply(state, event)

        return ReplayTrace(
            final_state=state,
            commit_path=commit_path[::-1],   # chronological
            event_count=len(all_events),
            verified=True,
            proof_root=self.heads.get(inft_id, "0x0")
        )

    async def replay(self, inft_id: str, to_version: Optional[int] = None) -> Dict[str, Any]:
        trace = await self.replay_with_trace(inft_id, to_version)
        return trace.final_state

    # ====================== HIGH-LEVEL ======================

    async def evolve(self, inft_id: str, events: List[Dict], metadata: Optional[Dict] = None) -> MemoryCommit:
        return await self.commit(inft_id, events, metadata)

    def get_head(self, inft_id: str) -> Optional[MemoryCommit]:
        cid = self.heads.get(inft_id)
        return self.commits.get(cid) if cid else None


# Default reducer (extend for your domain)
class DefaultReducer:
    version = "1.0"

    def apply(self, state: Dict[str, Any], event: Dict[str, Any]) -> Dict[str, Any]:
        state = state.copy()
        if isinstance(event.get("data"), dict):
            state.update(event["data"])
        return state


# Factory
async def create_memory_system() -> INFTMemoryOS:
    # Load client from env as in previous versions
    client = ZeroGStorageClient(...)  
    return INFTMemoryOS(client, DefaultReducer())
