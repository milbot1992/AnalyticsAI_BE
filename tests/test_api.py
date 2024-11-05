import pytest
from fastapi.testclient import TestClient
from app import app 

client = TestClient(app)

# Mock data that would typically be in processed_data.csv
MOCK_DATA = {
    "Area Name": ["Manchester", "York"],
    "Indicator Name": ["Under 75 mortality rate from cancer", "Life expectancy at birth"],
    "Value": [170.05582, 81.25],
    "Lower CI 95.0 limit": [161.57734, 79.0],
    "Upper CI 95.0 limit": [178.8565, 83.0],
    "Compared to England value or percentiles": ["Worse", "Better"],
    "gpt_commentary": [
        "- The Under 75 mortality rate from cancer for Local Authority Manchester is higher than average, with a value of 170.1. \n- The z-score of 1.72 indicates that this measure is somewhat uncommon compared to other Local Authorities.\n- The 95% confidence interval for this measure is from 161.6 to 178.9, suggesting some variability in the data.\n- This Local Authority may benefit from further investigation into potential factors contributing to the higher mortality rate from cancer.\n\nOverall, Local Authority Manchester exhibits a higher than average Under 75 mortality rate from cancer compared to other areas, indicating a potential area for targeted health interventions.",
        "- The life expectancy at birth for Local Authority York is 81.25 years, which is above average. \n- This figure suggests a favorable health environment, with a 95% confidence interval indicating variability between 79.0 and 83.0 years.\n- Compared to other areas, this indicates a positive health outcome for residents."
    ]
}

@pytest.fixture
def mock_data(monkeypatch):
    # Mock data same format as the CSV
    import pandas as pd
    mock_df = pd.DataFrame(MOCK_DATA)
    monkeypatch.setattr("pandas.read_csv", lambda *args, **kwargs: mock_df)

def test_available_options(mock_data):
    response = client.get("/available_options")
    assert response.status_code == 200
    assert set(response.json()["Area Names"]) == set(["Manchester", "York"])
    assert response.json()["Indicator Names"] == ["Under 75 mortality rate from cancer", "Life expectancy at birth"]

def test_get_local_authority_data(mock_data):
    response = client.get("/local_authority/Manchester?indicator_name=Under 75 mortality rate from cancer")
    assert response.status_code == 200
    assert response.json() == {
        "Area Name": "Manchester",
        "Indicator Name": "Under 75 mortality rate from cancer",
        "GPT Commentary": MOCK_DATA["gpt_commentary"][0],
        "Data Points": {
            "Value": 170.05582,
            "Lower CI 95.0 limit": 161.57734,
            "Upper CI 95.0 limit": 178.8565,
            "Compared to England value or percentiles": "Worse"
        }
    }

def test_get_local_authority_data_not_found():
    response = client.get("/local_authority/UnknownArea?indicator_name=Under 75 mortality rate from cancer")
    assert response.status_code == 404
    assert response.json() == {"detail": "No data found for Local Authority 'UnknownArea' with Indicator 'Under 75 mortality rate from cancer'."}
