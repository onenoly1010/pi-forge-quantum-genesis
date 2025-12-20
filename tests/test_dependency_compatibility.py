"""
Test to verify that all required dependencies can be imported together
without version conflicts, specifically the FastAPI and Gradio compatibility issue.
"""
import pytest


def test_fastapi_gradio_compatibility():
    """Test that FastAPI and Gradio can be imported together without conflicts."""
    try:
        import fastapi
        import gradio
        
        # Verify FastAPI version meets Gradio's requirements (>=0.115.2)
        fastapi_version = fastapi.__version__
        major, minor, patch = map(int, fastapi_version.split('.')[:3])
        
        assert major == 0, f"FastAPI major version should be 0, got {major}"
        assert minor >= 115 or major > 0, f"FastAPI version should be >=0.115.2, got {fastapi_version}"
        
        print(f"✅ FastAPI version {fastapi_version} is compatible with Gradio")
        print(f"✅ Gradio version {gradio.__version__} imported successfully")
        
    except ImportError as e:
        pytest.fail(f"Failed to import dependencies: {e}")


def test_all_main_dependencies():
    """Test that all main dependencies can be imported."""
    dependencies = [
        'fastapi',
        'uvicorn',
        'supabase',
        'websockets',
        'pydantic',
        'httpx',
        'flask',
        'flask_cors',
        'gradio',
        'dotenv',
        'aiohttp',
        'schedule',
        'psutil',
        'pytest',
        'pandas',
        'numpy',
    ]
    
    failed_imports = []
    for dep in dependencies:
        try:
            if dep == 'dotenv':
                __import__('dotenv')
            elif dep == 'flask_cors':
                __import__('flask_cors')
            else:
                __import__(dep)
        except ImportError as e:
            failed_imports.append((dep, str(e)))
    
    if failed_imports:
        error_msg = "Failed to import the following dependencies:\n"
        for dep, error in failed_imports:
            error_msg += f"  - {dep}: {error}\n"
        pytest.fail(error_msg)
    
    print(f"✅ All {len(dependencies)} main dependencies imported successfully")


def test_fastapi_version_range():
    """Test that FastAPI version is within the acceptable range."""
    import fastapi
    
    version = fastapi.__version__
    major, minor, patch = map(int, version.split('.')[:3])
    
    # Should be >= 0.115.2 and < 0.125
    assert major == 0, f"FastAPI major version should be 0, got {major}"
    assert 115 <= minor < 125, f"FastAPI minor version should be between 115 and 124, got {minor}"
    
    print(f"✅ FastAPI version {version} is within acceptable range (>=0.115.2, <0.125)")


def test_gradio_version_range():
    """Test that Gradio version is within the acceptable range."""
    import gradio
    
    version = gradio.__version__
    major, minor = map(int, version.split('.')[:2])
    
    # Should be >= 5.24.0 and < 5.32
    assert major == 5, f"Gradio major version should be 5, got {major}"
    assert 24 <= minor < 32, f"Gradio minor version should be between 24 and 31, got {minor}"
    
    print(f"✅ Gradio version {version} is within acceptable range (>=5.24.0, <5.32)")
