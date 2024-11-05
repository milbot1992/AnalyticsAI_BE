import pandas as pd
from Data.api import fetch_indicator_data
from Data.analysis import calculate_statistics
from Data.gpt_analysis import generate_gpt_commentary

def main():
    # Define indicators to be used
    indicator_ids = [40501, 90366]

    # Step 1: Fetch data and for now filter to just 'Persons' and keep for just 2 LAs
    combined_data = fetch_indicator_data(indicator_ids)

    # Step 2: Calculate statistical metrics and save to csv
    stats_data = calculate_statistics(combined_data)

    # Step 3: Generate GPT commentary for each Local Authority
    data_with_commentary = generate_gpt_commentary(stats_data)

    # Step 4: Save the processed data with GPT commentary
    data_with_commentary.to_csv('Data/processed_data.csv', index=False)
    print("Data processed and saved to 'Data/processed_data.csv'")

if __name__ == "__main__":
    main()
