import requests
import pandas as pd
from io import StringIO

def fetch_data():
    url = "https://fingertips.phe.org.uk/api/all_data/csv/for_one_indicator"
    params = {'indicator_id': 40501}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # Reading CSV data from response content
        data = pd.read_csv(StringIO(response.content.decode('utf-8')))
        
        # Filtering data where "Time period" is "2020 - 22" & "Category Type" is null
        filtered_data = data[(data['Time period'] == '2020 - 22') & (data['Category Type'].isnull())]
        # For now reduce date to Persons and just for 2 LAs
        filtered_data_2 = filtered_data[(filtered_data['Sex'] == 'Persons') & (filtered_data['Area Name'].isin(['Manchester', 'York']))]
        # Only keep necessary fields
        reduced_data = 
        
        return filtered_data
    else:
        raise Exception("Failed to fetch data. Status code:", response.status_code)

try:
    filtered_data = fetch_data()
    print('API data:', filtered_data.head())
except Exception as e:
    print(e)
