from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.analytics.cpi.routes import router

api = FastAPI()
api.include_router(router)

client = TestClient(api)


def test_calculate_au_annualised_cpi():
    response = client.get("/api/annualised_cpi/au")
    analytics_data = response.json()['data']
    assert response.status_code == 200
    assert 'annualised_cpi' in analytics_data[0], "Result should have 'annualised_cpi' field"

    for entry in analytics_data:
        assert 'time_period' in entry, "Each entry should have 'time_period' field"
        assert isinstance(entry['time_period'], str)
        assert 'annualised_cpi' in entry, "Each entry should have 'annualised_cpi' field"
        assert isinstance(entry['annualised_cpi'], float)


def test_calculate_uk_annualised_cpi():
    response = client.get("/api/annualised_cpi/uk")
    analytics_data = response.json()['data']
    assert response.status_code == 200
    assert 'annualised_cpi' in analytics_data[0], "Result should have 'annualised_cpi' field"

    for entry in analytics_data:
        assert 'time_period' in entry, "Each entry should have 'time_period' field"
        assert isinstance(entry['time_period'], str)
        assert 'annualised_cpi' in entry, "Each entry should have 'annualised_cpi' field"
        assert isinstance(entry['annualised_cpi'], float)
