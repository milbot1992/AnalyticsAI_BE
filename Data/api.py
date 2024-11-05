import requests
import pandas as pd
from io import StringIO

def fetch_indicator_data(indicator_ids):
    """
    Fetch and process data for a list of indicator IDs from the PHE API.

    Parameters:
        indicator_ids (list): A list of indicator IDs to retrieve data for.

    Returns:
        pd.DataFrame: A combined DataFrame with filtered and processed data for the specified indicators.
    """
    all_data_frames = []
    base_url = "https://fingertips.phe.org.uk/api/all_data/csv/for_one_indicator"

    for indicator_id in indicator_ids:
        # Set up request parameters
        params = {'indicator_id': indicator_id}
        response = requests.get(base_url, params=params)
        
        # Proceed if the request is successful
        if response.status_code == 200:
            # Read CSV data directly from the response content
            raw_data = pd.read_csv(StringIO(response.content.decode('utf-8')))
            
            # Filter data for specific time period and null 'Category Type'
            filtered_data = raw_data[(raw_data['Time period'] == '2020 - 22') & 
                                     (raw_data['Category Type'].isnull())]
            
            # Further filter for rows where area is 'Manchester' or 'York'
            area_filtered_data = filtered_data[(filtered_data['Area Name'].isin(['Manchester', 'York']))]
            
            # Additional filter if indicator ID is 40501
            if indicator_id == 40501:
                area_filtered_data = area_filtered_data[area_filtered_data['Sex'] == 'Persons']
            
            # Select only the relevant columns
            reduced_data = area_filtered_data[['Area Name', 'Area Code', 'Value', 'Indicator Name', 
                                               'Indicator ID', 'Lower CI 95.0 limit', 'Upper CI 95.0 limit', 
                                               'Compared to England value or percentiles', 'Denominator', 
                                               'Count', 'Sex']]
            
            # Append processed DataFrame to the list
            all_data_frames.append(reduced_data)
        else:
            print(f"Failed to fetch data for indicator {indicator_id}. HTTP Status code:", response.status_code)
    
    # Concatenate all data frames for the different indicators into one
    combined_data = pd.concat(all_data_frames, ignore_index=True)
    return combined_data
