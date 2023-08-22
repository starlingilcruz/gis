import json
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_app():
    response = client.get('/')

    assert response.status_code == 200

def test_display():
    response = client.get("/display/f1650f2a99824f349643ad234abff6a2")

    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/jpeg'

def test_display_raise_404_not_found():
    response = client.get("/display/doesnotexists")

    assert response.status_code == 404
    assert response.headers['content-type'] == 'application/json'

def test_display_overlay():
    response = client.get("/display/f1650f2a99824f349643ad234abff6a2/overlays")

    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/jpeg'

def test_display_overlay_raise_404_not_found():
    response = client.get("/display/doesnotexists/overlays")

    assert response.status_code == 404
    assert response.headers['content-type'] == 'application/json'

def test_post_find():
    payload = {
        "location": {
            "type": "Point",
            "coordinates": [-80.0782213, 26.8849731]
        },
        "distance_m": 100
    }
    expected = [
        {
            "property_id": "3290ec7dd190478aab124f6f2f32bdd7",
            "distance_m": 0.0
        }
    ]
    response = client.post("/find",json.dumps(payload))

    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert response.json() == expected

def test_display_overlay_raise_404_not_found():
    response = client.get("/display/doesnotexists/overlays")

    assert response.status_code == 404
    assert response.headers['content-type'] == 'application/json'

def test_get_property_statistic():
    response = client.get("/statistics/f1650f2a99824f349643ad234abff6a2?zone_size_m=10")
    
    assert response.status_code == 200
    assert response.json() == {
        'parcel_area_sqm': 911.8299704492092, 
        'building_area_sqm': 265.53881582338363, 
        'building_distance_m': 1.39289334, 
        'zone_density': 78.54188703946024
    }

def test_get_property_statistic_raise_404_not_found():
    response = client.get("/statistics/doesnotexists?zone_size_m=10")
    assert response.status_code == 404
    assert response.headers['content-type'] == 'application/json'