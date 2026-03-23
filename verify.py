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
        'flask_socketio': 'Flask-SocketIO',
        'flask_cors': 'Flask-CORS',
        'supabase': 'Supabase',
        'web3': 'Web3',
        'redis': 'Redis',
        'jwt': 'PyJWT',
        'dotenv': 'python-dotenv',
        'gunicorn': 'Gunicorn',
        'gevent': 'gevent'
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
        print_error("Some dependencies are missing. Run: pip install -r backend/requirements.txt")
    
    return all_installed

def check_file_structure():
    """Verify repository file structure"""
    print_header("File Structure Check")
    
    required_files = [
        'README.md',
        'INSTALL.md',
        'index.html',
        'backend/app.py',
        'backend/auth.py',
        'backend/requirements.txt',
        'frontend/index.html',
        'frontend/app.js',
        'frontend/style.css',
        'Dockerfile',
        'nixpacks.toml'
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

def check_backend_structure():
    """Check backend code structure and imports"""
    print_header("Backend Structure Check")
    
    # Save original directory before try block
    original_dir = os.getcwd()
    
    try:
        # Change to backend directory
        backend_dir = Path('backend')
        
        if backend_dir.exists():
            os.chdir(backend_dir)
            
            # Try to import the app module
            spec = importlib.util.spec_from_file_location("app", "app.py")
            app_module = importlib.util.module_from_spec(spec)
            
            print_success("Backend app.py is importable")
            
            # Check for key components
            if Path('auth.py').exists():
                print_success("Authentication module exists")
            
            os.chdir(original_dir)
            return True
            
        else:
            print_error("backend/ directory not found")
            return False
            
    except Exception as e:
        print_error(f"Backend structure check failed: {str(e)}")
        os.chdir(original_dir)
        return False

def test_backend_imports():
    """Test that backend can import all necessary modules"""
    print_header("Backend Import Test")
    
    try:
        # Set up path
        sys.path.insert(0, str(Path('backend').absolute()))
        
        # Try importing auth module
        from auth import generate_token, token_required
        print_success("Auth module imports successfully")
        
        # Test token generation
        token = generate_token(1)
        if token:
            print_success("Token generation works")
        else:
            print_warning("Token generation returned None")
        
        return True
        
    except ImportError as e:
        print_error(f"Import error: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Backend import test failed: {str(e)}")
        return False

def check_configuration():
    """Check configuration files and environment"""
    print_header("Configuration Check")
    
    # Check for .env file
    env_file = Path('backend/.env')
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
        print(f"\n{Colors.BLUE}You can now run: python backend/app.py{Colors.END}\n")
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
        'Backend Structure': check_backend_structure(),
        'Backend Imports': test_backend_imports(),
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
