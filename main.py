import pandas as pd
from Data.api import fetch_data
from Data.analysis import calculate_statistics
from Data.gpt_analysis import generate_gpt_commentary

def main():
    # Step 1: Fetch data and for now filter to just 'Persons'
    # data = fetch_data()
    # persons_data = data[(data['Sex'] == 'Persons')]

    # Step 2: Calculate statistical metrics and save to csv
    # stats_data = calculate_statistics(persons_data)

    # Step 3: Generate GPT commentary for each Local Authority
    #csv_file_path = 'Data/indicator_data_20_22.csv'
    #data = pd.read_csv(csv_file_path)
    #data = generate_gpt_commentary(data)

    # Step 3: Generate GPT commentary for each Local Authority
    csv_file_path = 'Data/Manchester_data_20_22.csv'
    data = pd.read_csv(csv_file_path)
    manchester_data = data[(data['Area Name'] == 'Manchester')]
    data = generate_gpt_commentary(manchester_data)

    # Step 4: Save the processed data with GPT commentary
    data.to_csv('Data/processed_data.csv', index=False)
    print("Data processed and saved to 'Data/processed_data.csv'")

if __name__ == "__main__":
    main()
