import pandas as pd
import os

def calculate_statistics():
    # Load data from the CSV file
    input_file = 'data/raw_data.csv'
    data = pd.read_csv(input_file)

    # z-score for each Local Authority
    data['z_score'] = (data['Value'] - data['Value'].mean()) / data['Value'].std()
    
    # Boolean if within one or two standard deviations of the mean
    data['within_1_std'] = (abs(data['z_score']) <= 1)
    data['within_2_std'] = (abs(data['z_score']) <= 2)
    
    # Width of the 95% confidence intervals for additional context
    data['CI_95_width'] = data['Upper CI 95.0 limit'] - data['Lower CI 95.0 limit']

    # Define the ranking order for each indicator
    ranking_order = {
        40501: False,  # Descending rank (higher values rank 1)
        90366: True,  # Ascending rank (lower values rank 1) 
        90362: True,
        93562: True,
        92901: False, 
        93505: True,
        91102: True,
        93523: True,
        93190: False,
    }

    # Ranking logic
    def rank_data(group):
        ascending = ranking_order.get(group['Indicator ID'].iloc[0], True)
        indicator_id = group['Indicator ID'].iloc[0]
        if indicator_id == 40501:
            group['rank'] = group['Value'].rank(ascending=ascending, method='min')
        else:
            group['rank'] = group.groupby('Sex')['Value'].rank(ascending=ascending, method='min')
        return group
    
    # Apply ranking to each group
    data = data.groupby('Indicator ID', group_keys=False).apply(rank_data)
    
    # Save the processed data to a CSV file
    output_directory = 'data'
    output_filename = 'analysed_data.csv'
    output_path = os.path.join(output_directory, output_filename)
    os.makedirs(output_directory, exist_ok=True)
    data.to_csv(output_path, index=False)

    print(f'Analysis data saved to {output_path}')

    return data

calculate_statistics()