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