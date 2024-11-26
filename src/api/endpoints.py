from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Load data once when the application starts
DATA_FILE_PATH = os.path.join(os.getcwd(), 'data', 'processed_data.csv')
try:
    data = pd.read_csv(DATA_FILE_PATH)
except FileNotFoundError:
    raise RuntimeError(f"Data file not found at {DATA_FILE_PATH}. Please check the file path.")

def fetch_filtered_data(la_name: str, indicator_name: str) -> pd.Series:
    """Fetches data row for a specific Local Authority and Indicator.
    
    Args:
        la_name (str): The name of the Local Authority.
        indicator_name (str): The name of the Indicator.

    Returns:
        pd.Series: The first matching data row.

    Raises:
        HTTPException: If no matching data is found.
    """
    filtered_data = data[(data['Area Name'] == la_name) & (data['Indicator Name'] == indicator_name)]
    if filtered_data.empty:
        raise HTTPException(
            status_code=404, 
            detail=f"No data found for Local Authority '{la_name}' with Indicator '{indicator_name}'."
        )
    return filtered_data.iloc[0]

@app.get("/local_authority/{la_name}")
def get_local_authority_data(
    la_name: str,
    indicator_name: str = Query(..., alias="indicator_name", description="Name of the Indicator to retrieve data for.")
):
    """Endpoint to retrieve data and GPT commentary for a specified Local Authority and Indicator.
    
    Args:
        la_name (str): Local Authority name passed as a path parameter.
        indicator_name (str): Indicator name passed as a query parameter.

    Returns:
        dict: Contains Local Authority data and analysis.
    """
    # Retrieve data
    la_data = fetch_filtered_data(la_name, indicator_name)

    # Format and return the response
    return {
        "Area Name": la_data['Area Name'],
        "Indicator Name": la_data['Indicator Name'],
        "GPT Commentary": la_data['gpt_commentary'],
        "Data Points": {
            "Value": la_data['Value'],
            "Lower CI 95.0 limit": la_data['Lower CI 95.0 limit'],
            "Upper CI 95.0 limit": la_data['Upper CI 95.0 limit'],
            "Compared to England value or percentiles": la_data['Compared to England value or percentiles']
        }
    }

@app.get("/available_options")
def get_available_options():
    """Endpoint to retrieve lists of available Area Names and Indicator Names."""
    area_names = data['Area Name'].unique().tolist()
    indicator_names = data['Indicator Name'].unique().tolist()

    return {
        "Area Names": area_names,
        "Indicator Names": indicator_names
    }
