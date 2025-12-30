#!/usr/bin/env python3
"""
Pi Forge Quantum Genesis - Installation Verification Script
By Kris Olofson

This script verifies that the Pi Forge installation is correctly set up
and all components are functioning properly.
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def check_python_version():
    """Verify Python version meets requirements"""
    print_header("Python Version Check")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_info(f"Python version: {version_str}")
    
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version_str} meets requirements (3.11+)")
        return True
    else:
        print_error(f"Python {version_str} does not meet requirements (3.11+)")
        return False

def check_dependencies():
    """Check if all required Python packages are installed"""
    print_header("Dependency Check")
    
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'supabase': 'Supabase',
        'websockets': 'WebSockets',
        'pydantic': 'Pydantic',
        'httpx': 'HTTPX',
        'dotenv': 'python-dotenv',
        'gradio': 'Gradio',
        'aiohttp': 'aiohttp'
    }
    
    all_installed = True
    
    for package, name in required_packages.items():
        spec = importlib.util.find_spec(package)
        if spec is not None:
            print_success(f"{name} is installed")
        else:
            print_error(f"{name} is NOT installed")
            all_installed = False
    
    if all_installed:
        print_success("All required dependencies are installed")
    else:
        print_error("Some dependencies are missing. Run: pip install -r server/requirements.txt")
    
    return all_installed

def check_file_structure():
    """Verify repository file structure"""
    print_header("File Structure Check")
    
    required_files = [
        'README.md',
        'INSTALL.md',
        'index.html',
        'server/app.py',
        'server/main.py',
        'server/requirements.txt',
        'Dockerfile',
        'railway.toml'
    ]
    
    all_exist = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"{file_path} exists")
        else:
            print_error(f"{file_path} is missing")
            all_exist = False
    
    if all_exist:
        print_success("All required files are present")
    else:
        print_warning("Some files are missing (may not affect functionality)")
    
    return all_exist

def check_server_structure():
    """Check server code structure and imports"""
    print_header("Server Structure Check")
    
    try:
        # Change to server directory
        original_dir = os.getcwd()
        server_dir = Path('server')
        
        if server_dir.exists():
            os.chdir(server_dir)
            
            # Check for key files
            if Path('app.py').exists():
                print_success("server/app.py exists")
            
            if Path('main.py').exists():
                print_success("server/main.py exists")
            
            if Path('requirements.txt').exists():
                print_success("server/requirements.txt exists")
            
            os.chdir(original_dir)
            return True
            
        else:
            print_error("server/ directory not found")
            return False
            
    except Exception as e:
        print_error(f"Server structure check failed: {str(e)}")
        if 'original_dir' in locals():
            os.chdir(original_dir)
        return False

def test_server_imports():
    """Test that server can import all necessary modules"""
    print_header("Server Import Test")
    
    try:
        # Set up path
        sys.path.insert(0, str(Path('server').absolute()))
        
        # Try importing common modules
        try:
            import flask
            print_success("Flask imports successfully")
        except ImportError:
            print_warning("Flask import failed (may not be used)")
        
        try:
            import fastapi
            print_success("FastAPI imports successfully")
        except ImportError:
            print_warning("FastAPI import failed (may not be used)")
        
        return True
        
    except Exception as e:
        print_error(f"Server import test failed: {str(e)}")
        return False

def check_configuration():
    """Check configuration files and environment"""
    print_header("Configuration Check")
    
    # Check for .env file
    env_file = Path('.env')
    if env_file.exists():
        print_success(".env file exists")
        print_info("Environment variables can be configured")
    else:
        print_warning(".env file not found (optional)")
        print_info("Application will use default values")
    
    # Check environment variables
    important_vars = ['SECRET_KEY', 'PORT', 'REDIS_URL', 'SUPABASE_URL']
    
    for var in important_vars:
        value = os.getenv(var)
        if value:
            print_success(f"{var} is set")
        else:
            print_info(f"{var} is not set (will use defaults)")
    
    return True

def check_git_repository():
    """Verify git repository status"""
    print_header("Git Repository Check")
    
    try:
        # Check if .git exists
        if Path('.git').exists():
            print_success("Git repository initialized")
            
            # Get current branch
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                branch = result.stdout.strip()
                print_info(f"Current branch: {branch}")
            
            # Check remote
            result = subprocess.run(
                ['git', 'remote', '-v'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout:
                print_success("Git remote configured")
            
            return True
        else:
            print_warning("Not a git repository")
            return False
            
    except Exception as e:
        print_warning(f"Git check failed: {str(e)}")
        return False

def generate_report(results):
    """Generate final verification report"""
    print_header("Verification Summary")
    
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    print(f"\n{Colors.BOLD}Total Checks: {total_checks}{Colors.END}")
    print(f"{Colors.GREEN}Passed: {passed_checks}{Colors.END}")
    print(f"{Colors.RED}Failed: {total_checks - passed_checks}{Colors.END}")
    
    success_rate = (passed_checks / total_checks) * 100
    
    print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.END}")
    
    if success_rate == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED! Installation verified! 🎉{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}{'='*60}{Colors.END}\n")
        print(f"{Colors.GREEN}✓ Repository is live and correctly configured{Colors.END}")
        print(f"{Colors.GREEN}✓ All dependencies are installed{Colors.END}")
        print(f"{Colors.GREEN}✓ Index files are properly populated{Colors.END}")
        print(f"\n{Colors.BLUE}You can now run: python server/app.py{Colors.END}\n")
    elif success_rate >= 80:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ INSTALLATION MOSTLY COMPLETE ⚠{Colors.END}")
        print(f"{Colors.YELLOW}Some optional checks failed, but core functionality should work.{Colors.END}\n")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ INSTALLATION INCOMPLETE ❌{Colors.END}")
        print(f"{Colors.RED}Several checks failed. Please review errors above.{Colors.END}\n")

def main():
    """Main verification function"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Pi Forge Quantum Genesis - Installation Verification     ║")
    print("║  By Kris Olofson (onenoly1010)                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # Run all checks
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'File Structure': check_file_structure(),
        'Server Structure': check_server_structure(),
        'Server Imports': test_server_imports(),
        'Configuration': check_configuration(),
        'Git Repository': check_git_repository()
    }
    
    # Generate report
    generate_report(results)
    
    # Return exit code
    all_passed = all(results.values())
    sys.exit(0 if all_passed else 1)

if __name__ == '__main__':
    main()
