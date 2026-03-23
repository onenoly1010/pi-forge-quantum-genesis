"""Run tests and save output to file"""
import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

result = subprocess.run(
    [r".venv\Scripts\pytest.exe", 
     "tests/test_genesis_references.py",
     "tests/test_vercel_build.py",
     "-v"],
    capture_output=True,
    text=True,
    timeout=60
)

with open("test_results.txt", "w") as f:
    f.write("=== STDOUT ===\n")
    f.write(result.stdout)
    f.write("\n=== STDERR ===\n")
    f.write(result.stderr)
    f.write(f"\n=== RETURN CODE: {result.returncode} ===\n")

print("Test results written to test_results.txt")
print(f"Return code: {result.returncode}")
