from fastapi import FastAPI, HTTPException
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

# Load the processed data with GPT commentary
data = pd.read_csv(os.path.join(os.getcwd(), 'Data', 'processed_data.csv'))

@app.get("/local_authority/{la_name}")
def get_local_authority_data(la_name: str):
    la_data = data[data['Area Name'] == la_name]
    if la_data.empty:
        raise HTTPException(status_code=404, detail="Local Authority not found")

    return {
        'Area Name': la_data['Area Name'].iloc[0],
        'Indicator Name': la_data['Indicator Name'].iloc[0],
        'GPT Commentary': la_data['gpt_commentary'].iloc[0],
        'Data Points': {
            'Value': la_data['Value'].iloc[0],
            'Lower CI 95.0 limit': la_data['Lower CI 95.0 limit'].iloc[0],
            'Upper CI 95.0 limit': la_data['Upper CI 95.0 limit'].iloc[0],
            'Compared to England value or percentiles': la_data['Compared to England value or percentiles'].iloc[0]
    }
}