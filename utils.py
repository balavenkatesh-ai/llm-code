from fastapi.testclient import TestClient
from app import app  # Replace this with your actual app import

client = TestClient(app)

# Test for GET `/tip/control_remediation/{gts_id}`
def test_get_tip_controls_by_gts_id():
    gts_id = "test_id"  # Replace with a valid ID
    response = client.get(f"/tip/control_remediation/{gts_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"  # Adjust this based on your actual response

# Test for GET `/tip/control_remediation/`
def test_get_all_tip_controls():
    response = client.get("/tip/control_remediation/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Assuming it returns a list of controls

# Test for POST `/tip/inventory`
def test_save_tip_inventory():
    inventory_data = {
        "field1": "value1",  # Replace with actual fields
        "field2": "value2",
        # Add more fields as required by your model
    }
    response = client.post("/tip/inventory", json=inventory_data)
    assert response.status_code == 200
    assert response.json()["message"] == "TIP Inventory Successfully Created in the Database"