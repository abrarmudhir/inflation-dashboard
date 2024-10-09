from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.data.cpi.routes import router

api = FastAPI()
api.include_router(router)

client = TestClient(api)


def test_get_uk_cpi_data():
    response = client.get("/api/cpi/uk")
    data = response.json()['data']
    assert response.status_code == 200
    assert len(data) > 0, "UK CPI data should not be empty"
    assert all('time_period' in record for record in data), "Each record should have 'time_period'"
    assert all('value' in record for record in data), "Each record should have 'value'"
    assert all('frequency' in record for record in data), "Each record should have 'frequency'"


def test_get_au_cpi_data():
    response = client.get("/api/cpi/au")
    data = response.json()['data']
    assert response.status_code == 200
    assert len(data) > 0, "AU CPI data should not be empty"
    assert all('time_period' in record for record in data), "Each record should have 'time_period'"
    assert all('value' in record for record in data), "Each record should have 'value'"
    assert all('frequency' in record for record in data), "Each record should have 'frequency'"


def test_invalid_country_code():
    response = client.get("/api/cpi/INVALID")
    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported country code"}, "Invalid country code should return 400 error"

