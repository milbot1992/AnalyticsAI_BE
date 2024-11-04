import pandas as pd
import os

def calculate_statistics(data):
    # Calculate the z-score for each Local Authority
    data['z_score'] = (data['Value'] - data['Value'].mean()) / data['Value'].std()
    
    # Calculate if the 'Value' is within one or two standard deviations of the mean
    data['within_1_std'] = (abs(data['z_score']) <= 1)
    data['within_2_std'] = (abs(data['z_score']) <= 2)
    
    # Calculate the width of the 95% and 99.8% confidence intervals for additional context
    data['CI_95_width'] = data['Upper CI 95.0 limit'] - data['Lower CI 95.0 limit']
    data['CI_99.8_width'] = data['Upper CI 99.8 limit'] - data['Lower CI 99.8 limit']
    
    print('Analysis data:', data.head())
    
    # Save the processed data to a CSV file
    output_directory = 'Data'
    output_filename = 'indicator_data_20_22.csv'
    output_path = os.path.join(output_directory, output_filename)
    os.makedirs(output_directory, exist_ok=True)
    data.to_csv(output_path, index=False)
    
    print(f'Data saved to {output_path}')

    return data
