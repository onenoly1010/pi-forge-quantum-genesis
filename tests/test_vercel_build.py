"""
Test suite for Vercel build process
Validates that the build script correctly generates the .vercel/output/static directory
"""
import os
import subprocess
import shutil
from pathlib import Path

import pytest


# Get the root directory of the repository
ROOT_DIR = Path(__file__).parent.parent


class TestVercelBuild:
    """Tests for Vercel build configuration and process"""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Clean up .vercel/output/static directory before and after tests"""
        output_dir = ROOT_DIR / ".vercel" / "output"
        
        # Clean before test
        if output_dir.exists():
            shutil.rmtree(output_dir)
        
        yield
        
        # Clean after test (optional - can comment out to inspect)
        if output_dir.exists():
            shutil.rmtree(output_dir)

    def test_build_creates_output_directory(self):
        """Test that npm run build creates the .vercel/output/static directory"""
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Build failed: {result.stderr}"
        
        output_dir = ROOT_DIR / ".vercel" / "output" / "static"
        assert output_dir.exists(), ".vercel/output/static directory was not created"
        assert output_dir.is_dir(), ".vercel/output/static path is not a directory"

    def test_build_copies_required_html_files(self):
        """Test that all required HTML files are copied to .vercel/output/static directory"""
        # Run the build
        subprocess.run(
            ["npm", "run", "build"],
            cwd=ROOT_DIR,
            capture_output=True,
            check=True
        )
        
        output_dir = ROOT_DIR / ".vercel" / "output" / "static"
        required_files = [
            "index.html",
            "ceremonial_interface.html",
            "resonance_dashboard.html",
            "spectral_command_shell.html",
        ]
        
        for filename in required_files:
            file_path = output_dir / filename
            assert file_path.exists(), f"{filename} not found in .vercel/output/static directory"
            assert file_path.is_file(), f"{filename} is not a file"

    def test_build_copies_javascript_files(self):
        """Test that JavaScript files are copied to .vercel/output/static directory"""
        # Run the build
        subprocess.run(
            ["npm", "run", "build"],
            cwd=ROOT_DIR,
            capture_output=True,
            check=True
        )
        
        output_dir = ROOT_DIR / ".vercel" / "output" / "static"
        js_file = output_dir / "pi-forge-integration.js"
        
        assert js_file.exists(), "pi-forge-integration.js not found in .vercel/output/static directory"
        assert js_file.is_file(), "pi-forge-integration.js is not a file"

    def test_build_copies_frontend_directory(self):
        """Test that the frontend directory is copied to .vercel/output/static directory"""
        # Run the build
        subprocess.run(
            ["npm", "run", "build"],
            cwd=ROOT_DIR,
            capture_output=True,
            check=True
        )
        
        output_dir = ROOT_DIR / ".vercel" / "output" / "static"
        frontend_dir = output_dir / "frontend"
        
        assert frontend_dir.exists(), "frontend directory not found in .vercel/output/static directory"
        assert frontend_dir.is_dir(), "frontend is not a directory"
        
        # Check that frontend directory has files
        frontend_files = list(frontend_dir.glob("*"))
        assert len(frontend_files) > 0, "frontend directory is empty"

    def test_vercel_build_output_api_config(self):
        """Test that Vercel Build Output API config is correctly generated"""
        # Run the build first
        subprocess.run(
            ["npm", "run", "build"],
            cwd=ROOT_DIR,
            capture_output=True,
            check=True
        )
        
        config_path = ROOT_DIR / ".vercel" / "output" / "config.json"
        
        assert config_path.exists(), "config.json not found in .vercel/output/"
        
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        assert "version" in config, "version not specified in config.json"
        assert config["version"] == 3, "version should be 3 for Build Output API v3"
        assert "routes" in config, "routes not specified in config.json"

    def test_package_json_build_script(self):
        """Test that package.json has correct build script"""
        package_json_path = ROOT_DIR / "package.json"
        
        assert package_json_path.exists(), "package.json not found"
        
        import json
        with open(package_json_path, 'r') as f:
            package = json.load(f)
        
        assert "scripts" in package, "scripts section not found in package.json"
        assert "build" in package["scripts"], "build script not found in package.json"
        assert "build:static" in package["scripts"], "build:static script not found in package.json"

    def test_node_version_compatibility(self):
        """Test that package.json specifies compatible Node.js version"""
        package_json_path = ROOT_DIR / "package.json"
        
        import json
        with open(package_json_path, 'r') as f:
            package = json.load(f)
        
        assert "engines" in package, "engines section not found in package.json"
        assert "node" in package["engines"], "node version not specified in package.json"
        
        # Verify that the version constraint is specified
        node_version = package["engines"]["node"]
        assert node_version, "Node.js version should be specified"

    def test_gitignore_excludes_vercel_output(self):
        """Test that .gitignore excludes the .vercel directory"""
        gitignore_path = ROOT_DIR / ".gitignore"
        
        assert gitignore_path.exists(), ".gitignore not found"
        
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        assert ".vercel" in gitignore_content, ".vercel should be in .gitignore"
