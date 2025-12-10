"""
Test Bootstrap Agent Functionality

This module tests the bootstrap agent components to ensure they work correctly.
"""

import os
import sys
import pytest
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestBootstrapStructure:
    """Test that bootstrap directory structure is correct."""
    
    def test_bootstrap_directory_exists(self):
        """Test that bootstrap directory exists."""
        bootstrap_dir = PROJECT_ROOT / "bootstrap"
        assert bootstrap_dir.exists(), "Bootstrap directory should exist"
        assert bootstrap_dir.is_dir(), "Bootstrap should be a directory"
    
    def test_bootstrap_scripts_exist(self):
        """Test that bootstrap scripts exist."""
        scripts = [
            "bootstrap/bootstrap.sh",
            "bootstrap/bootstrap.ps1",
        ]
        
        for script in scripts:
            script_path = PROJECT_ROOT / script
            assert script_path.exists(), f"{script} should exist"
            assert script_path.is_file(), f"{script} should be a file"
    
    def test_bootstrap_sh_executable(self):
        """Test that bootstrap.sh is executable on Unix systems."""
        if os.name != 'nt':  # Skip on Windows
            script_path = PROJECT_ROOT / "bootstrap" / "bootstrap.sh"
            assert os.access(script_path, os.X_OK), "bootstrap.sh should be executable"
    
    def test_documentation_exists(self):
        """Test that bootstrap documentation exists."""
        docs = [
            "bootstrap/README.md",
            "bootstrap/QUICKSTART.md",
            "bootstrap/DEPLOYMENT_GUIDE.md",
            "bootstrap/docs/AUTONOMOUS_OPERATIONS.md",
        ]
        
        for doc in docs:
            doc_path = PROJECT_ROOT / doc
            assert doc_path.exists(), f"{doc} should exist"
            assert doc_path.is_file(), f"{doc} should be a file"
    
    def test_templates_exist(self):
        """Test that configuration templates exist."""
        templates = [
            "bootstrap/templates/railway.toml.template",
            "bootstrap/templates/docker-compose.yml.template",
        ]
        
        for template in templates:
            template_path = PROJECT_ROOT / template
            assert template_path.exists(), f"{template} should exist"
            assert template_path.is_file(), f"{template} should be a file"


class TestBootstrapScriptContent:
    """Test that bootstrap scripts have correct content."""
    
    def test_bootstrap_sh_has_shebang(self):
        """Test that bootstrap.sh has proper shebang."""
        script_path = PROJECT_ROOT / "bootstrap" / "bootstrap.sh"
        with open(script_path, 'r') as f:
            first_line = f.readline()
            assert first_line.startswith('#!/bin/bash'), "Should have bash shebang"
    
    def test_bootstrap_sh_has_required_functions(self):
        """Test that bootstrap.sh has all required functions."""
        script_path = PROJECT_ROOT / "bootstrap" / "bootstrap.sh"
        with open(script_path, 'r') as f:
            content = f.read()
            
        required_functions = [
            'check_system_requirements',
            'setup_environment',
            'validate_infrastructure',
            'run_tests',
            'initialize_services',
            'prepare_deployment',
            'setup_autonomous_handoff',
            'generate_final_report',
        ]
        
        for func in required_functions:
            assert func in content, f"Should have {func} function"
    
    def test_bootstrap_ps1_has_required_functions(self):
        """Test that bootstrap.ps1 has all required functions."""
        script_path = PROJECT_ROOT / "bootstrap" / "bootstrap.ps1"
        with open(script_path, 'r') as f:
            content = f.read()
            
        required_functions = [
            'Test-SystemRequirements',
            'Initialize-Environment',
            'Test-Infrastructure',
            'Invoke-Tests',
            'Initialize-Services',
            'Initialize-Deployment',
        ]
        
        for func in required_functions:
            assert func in content, f"Should have {func} function"


class TestCriticalFiles:
    """Test that critical files required by bootstrap exist."""
    
    def test_critical_server_files_exist(self):
        """Test that critical server files exist."""
        critical_files = [
            "server/main.py",
            "server/app.py",
            "server/canticle_interface.py",
            "server/requirements.txt",
        ]
        
        for file in critical_files:
            file_path = PROJECT_ROOT / file
            assert file_path.exists(), f"{file} should exist"
    
    def test_deployment_files_exist(self):
        """Test that deployment files exist."""
        deployment_files = [
            "Dockerfile",
            "railway.toml",
            ".env.example",
        ]
        
        for file in deployment_files:
            file_path = PROJECT_ROOT / file
            assert file_path.exists(), f"{file} should exist"
    
    def test_env_example_has_required_vars(self):
        """Test that .env.example has required variables."""
        env_example = PROJECT_ROOT / ".env.example"
        with open(env_example, 'r') as f:
            content = f.read()
        
        required_vars = [
            'SUPABASE_URL',
            'SUPABASE_KEY',
            'JWT_SECRET',
        ]
        
        for var in required_vars:
            assert var in content, f".env.example should have {var}"


class TestDocumentation:
    """Test documentation quality."""
    
    def test_readme_has_quickstart(self):
        """Test that main README has quickstart section."""
        readme = PROJECT_ROOT / "README.md"
        with open(readme, 'r') as f:
            content = f.read()
        
        assert 'Quick Start' in content, "README should have Quick Start section"
        assert 'bootstrap' in content.lower(), "README should mention bootstrap"
    
    def test_quickstart_has_examples(self):
        """Test that QUICKSTART has platform-specific examples."""
        quickstart = PROJECT_ROOT / "bootstrap" / "QUICKSTART.md"
        with open(quickstart, 'r') as f:
            content = f.read()
        
        assert 'Linux/macOS' in content, "Should have Linux/macOS instructions"
        assert 'Windows' in content, "Should have Windows instructions"
        assert './bootstrap/bootstrap.sh' in content, "Should show bash script usage"
        assert 'bootstrap.ps1' in content, "Should show PowerShell script usage"
    
    def test_deployment_guide_has_platforms(self):
        """Test that deployment guide covers multiple platforms."""
        deployment = PROJECT_ROOT / "bootstrap" / "DEPLOYMENT_GUIDE.md"
        with open(deployment, 'r') as f:
            content = f.read()
        
        platforms = ['Railway', 'Docker', 'Manual']
        for platform in platforms:
            assert platform in content, f"Should have {platform} deployment instructions"


class TestGitignore:
    """Test that .gitignore is properly configured."""
    
    def test_gitignore_excludes_bootstrap_artifacts(self):
        """Test that .gitignore excludes bootstrap artifacts."""
        gitignore = PROJECT_ROOT / ".gitignore"
        with open(gitignore, 'r') as f:
            content = f.read()
        
        artifacts = [
            'bootstrap/bootstrap-*.log',
            'bootstrap/bootstrap-report-*.md',
            'logs/',
        ]
        
        for artifact in artifacts:
            assert artifact in content, f".gitignore should exclude {artifact}"
    
    def test_gitignore_excludes_env(self):
        """Test that .gitignore excludes .env files."""
        gitignore = PROJECT_ROOT / ".gitignore"
        with open(gitignore, 'r') as f:
            content = f.read()
        
        assert '.env' in content, ".gitignore should exclude .env"
        assert '.venv' in content, ".gitignore should exclude .venv"


class TestImports:
    """Test that critical imports work."""
    
    def test_fastapi_imports(self):
        """Test that FastAPI module can be imported."""
        try:
            sys.path.insert(0, str(PROJECT_ROOT / "server"))
            from main import app
            assert app is not None, "FastAPI app should be importable"
        except ImportError as e:
            pytest.skip(f"FastAPI dependencies not installed: {e}")
    
    def test_flask_imports(self):
        """Test that Flask module can be imported."""
        try:
            sys.path.insert(0, str(PROJECT_ROOT / "server"))
            from app import app
            assert app is not None, "Flask app should be importable"
        except ImportError as e:
            pytest.skip(f"Flask dependencies not installed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
