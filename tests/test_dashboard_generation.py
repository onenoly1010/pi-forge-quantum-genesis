#!/usr/bin/env python3
"""Test the dashboard generation script to verify the fix"""
import os
import sys

# Add parent directory (repo root) to Python path to import generate_dashboard
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)

def test_dashboard_generation_in_repo():
    """Test that the dashboard generates correctly in the actual repository"""
    
    # Import the generate_dashboard module
    import generate_dashboard
    
    # Constants for test thresholds
    MIN_CONTENT_LENGTH = 1000
    MAX_NAVIGATION_LINE = 100
    TRUNCATION_CHECK_LENGTH = 5000  # Check first 5000 chars for truncation markers
    
    # Generate the dashboard content
    content = generate_dashboard.generate_dashboard()
    
    # Verify content is not empty
    assert len(content) > MIN_CONTENT_LENGTH, "Dashboard content should be substantial"
    
    # Verify no truncation placeholders remain
    # Check a substantial portion of early content for truncation markers
    early_content = content[:TRUNCATION_CHECK_LENGTH]
    assert '...' not in early_content, "Should not have ellipsis truncation in early content"
    assert '[truncated]' not in content.lower(), "Should not have [truncated] markers"
    assert '<!-- truncated -->' not in content.lower(), "Should not have truncation comments"
    assert '(truncated)' not in content.lower(), "Should not have (truncated) markers"
    
    # Verify navigation section exists and is properly located
    assert '## 📑 Quick Navigation' in content, "Quick Navigation section should exist"
    
    # Verify the navigation appears early in the document
    lines = content.split('\n')
    nav_line = next((i for i, line in enumerate(lines) if '## 📑 Quick Navigation' in line), -1)
    assert nav_line != -1, "Navigation section should be found"
    assert nav_line < MAX_NAVIGATION_LINE, \
        f"Navigation should appear within first {MAX_NAVIGATION_LINE} lines, found at line {nav_line}"
    
    # Verify key sections exist
    assert '## 🧭 Prerequisites' in content, "Prerequisites section should exist"
    assert '## 🌐 Platform Overview' in content, "Platform Overview section should exist"
    
    # Verify directory creation code exists in the script
    script_path = os.path.join(repo_root, 'generate_dashboard.py')
    with open(script_path, 'r') as f:
        script_content = f.read()
    
    assert "os.makedirs('docs', exist_ok=True)" in script_content, "Script should have directory creation code"
    
    print("✅ All tests passed!")
    print(f"   - Dashboard content generated: PASS ({len(content)} chars)")
    print(f"   - No truncation placeholders: PASS")
    print(f"   - Navigation section exists: PASS")
    print(f"   - Navigation properly located at line {nav_line}: PASS")
    print(f"   - Directory creation code exists: PASS")
    print(f"   - Key sections present: PASS")

def test_actual_file_generation():
    """Test that the dashboard file can be generated and exists"""
    
    # Run the script from repo root using current Python interpreter
    import subprocess
    script_path = os.path.join(repo_root, 'generate_dashboard.py')
    result = subprocess.run([sys.executable, script_path], 
                          cwd=repo_root,
                          capture_output=True, text=True)
    
    assert result.returncode == 0, f"Script should run successfully: {result.stderr}"
    
    # Verify the file was created
    dashboard_file = os.path.join(repo_root, 'docs/DEPLOYMENT_DASHBOARD.md')
    assert os.path.exists(dashboard_file), "Dashboard file should be created"
    
    # Verify the file has content
    with open(dashboard_file, 'r') as f:
        file_content = f.read()
    
    assert len(file_content) > 1000, "Generated file should have substantial content"
    
    print("✅ File generation test passed!")
    print(f"   - Script executed successfully: PASS")
    print(f"   - Dashboard file created: PASS")
    print(f"   - File has {len(file_content)} characters: PASS")

if __name__ == '__main__':
    try:
        print("=" * 60)
        print("Testing Dashboard Generation Fix")
        print("=" * 60)
        print()
        
        print("Test 1: Content Generation")
        print("-" * 60)
        test_dashboard_generation_in_repo()
        print()
        
        print("Test 2: Actual File Generation")
        print("-" * 60)
        test_actual_file_generation()
        print()
        
        print("=" * 60)
        print("✅ All verification tests passed!")
        print("=" * 60)
        print()
        print("Summary of fixes verified:")
        print("  1. ✅ No truncation placeholders in generated content")
        print("  2. ✅ Navigation section properly relocated (early in document)")
        print("  3. ✅ Directory check code present (os.makedirs with exist_ok=True)")
        print("  4. ✅ Dashboard file successfully generated")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
