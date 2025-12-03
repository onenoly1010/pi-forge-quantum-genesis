import sys
import os
from pathlib import Path

# Add server directory to path for imports
server_dir = Path(__file__).parent.parent / "server"
sys.path.insert(0, str(server_dir))

from fastapi.testclient import TestClient
import pytest

# Import the FastAPI app from server.main
from main import app

client = TestClient(app)

def test_health_endpoint_returns_200_and_keys():
    response = client.get('/health')
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert 'supabase_connected' in data
    assert 'timestamp' in data


@pytest.mark.parametrize('path', ['/','/api/metrics'])
def test_additional_endpoints(path):
    resp = client.get(path)
    assert resp.status_code == 200
