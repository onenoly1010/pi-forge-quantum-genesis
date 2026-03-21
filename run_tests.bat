@echo off
cd /d "%~dp0"
echo Running tests...
".venv\Scripts\pytest.exe" tests/test_genesis_references.py tests/test_canon_of_closure.py tests/test_vercel_build.py -v
echo.
echo Test run complete.
