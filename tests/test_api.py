from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_optimize_route():
    payload = {
        "stops": [
            {"lat": 40.7128, "lng": -74.0060, "address": "New York"},
            {"lat": 34.0522, "lng": -118.2437, "address": "Los Angeles"}
        ]
    }
    
    # This might take ~2 seconds due to the sleep in the endpoint
    response = client.post("/api/v1/optimize", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "success"
    assert len(data["optimized_order"]) == 2
    # Verify reversal logic
    assert data["optimized_order"][0] == "Los Angeles"
    assert data["optimized_order"][1] == "New York"
    assert "route_id" in data
    assert "execution_time_seconds" in data
    assert data["total_distance_km"] > 0
