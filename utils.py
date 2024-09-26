import pytest
from fastapi.testclient import TestClient
from app.main import app  # Assuming your FastAPI app is in main.py

client = TestClient(app)

# Test for the /tip/control_remediation/{gts_id} endpoint
def test_get_mq_controls_route():
    gts_id = "sample_gts_id"  # Replace with a valid ID
    response = client.get(f"/tip/control_remediation/{gts_id}")
    assert response.status_code == 200
    assert response.json() is not None  # Add more assertions based on expected JSON structure

# Test for the /tip/control_remediation endpoint
def test_get_all_tip_controls_route():
    response = client.get("/tip/control_remediation/")
    assert response.status_code == 200
    assert response.json() is not None  # Add more assertions based on expected JSON structure
    
import pytest
import requests

BASE_URL = "http://localhost:8000"  # replace with your API base URL

@pytest.fixture(scope='session')
def auth_token():
    """Fixture to authenticate and return the token."""
    url = f"{BASE_URL}/tip/api/v1/auth/login"
    payload = {
        "userId": "g.adopacc.001.dev",  # replace with valid userId
        "password": "SCBFirewallpace2024$"  # replace with valid password
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200, "Authentication failed"
    
    token = response.json().get("data").get("access_token")
    return token

def test_get_authenticated_api(auth_token):
    """Test authenticated API with the token."""
    url = f"{BASE_URL}/tip/api/v1/tip/control_remediation/GTS-4575"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Failed with status {response.status_code}"
    assert response.json() is not None