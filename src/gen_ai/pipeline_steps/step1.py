import pandas as pd

def find_important_indicators(local_authority, area_code):
    """
    Identify the worst indicators for a given local authority compared to other local authorities and England's average.

    Args:
        local_authority (str): Name of the local authority.
        area_code (str): Area code of the local authority.

    Returns:
        pd.DataFrame: A DataFrame with the worst indicators and reasons for their selection.
    """
    # Load the dataset
    data_path = 'data/analysed_data.csv'
    df = pd.read_csv(data_path)
    
    # Filter data for the given local authority
    local_data = df[(df['Area Name'] == local_authority) & (df['Area Code'] == area_code)]
    
    # Filter rows where "Compared to England value or percentiles" is "Worse"
    worse_indicators = local_data[local_data['Compared to England value or percentiles'] == 'Worse']
    
    # Create a list to store selected indicators with reasons
    selected_indicators = []
    
    for _, row in worse_indicators.iterrows():
        reasons = []
        
        # Automatically select if rank is in bottom 5% (Rank 1-15)
        if row['rank'] <= 15:
            reasons.append("Ranked among the 15 worst-performing local authorities compared to others.")
        # Additional criteria for selection
        if row['z_score'] > 2:
            reasons.append("Significant deviation from England average (high z_score).")
        if not row['within_1_std']:
            reasons.append("Outside 1 standard deviation from mean.")
        if row['CI_95_width'] > 20:  # Example threshold for wide confidence interval
            reasons.append("Wide confidence interval.")
        
        # Add to selection if any reasons are determined
        if reasons:
            selected_indicators.append({
                "Area Name": row['Area Name'],
                "Area Code": row['Area Code'],
                "Indicator Name": row['Indicator Name'],
                "Indicator ID": row['Indicator ID'],
                "Value": row['Value'],
                "Sex": row['Sex'],
                "Lower CI 95.0 limit": row['Lower CI 95.0 limit'],
                "Upper CI 95.0 limit": row['Upper CI 95.0 limit'],
                "Compared to England value or percentiles": row['Compared to England value or percentiles'],
                "within_1_std": row['within_1_std'],
                "within_2_std": row['within_2_std'],
                "rank": row['rank'],
                "z_score": row['z_score'],
                "Time period": row['Time period'],
                "reasons": reasons
            })
    
    # Convert the list of selected indicators to a DataFrame
    output_df = pd.DataFrame(selected_indicators)
    
    # Split reasons into separate columns (reason_1, reason_2, etc.)
    max_reasons = output_df['reasons'].apply(len).max() if not output_df.empty else 0
    for i in range(max_reasons):
        output_df[f'reason_{i+1}'] = output_df['reasons'].apply(lambda x: x[i] if i < len(x) else None)
    
    # Drop the "reasons" column as it's now split into individual columns
    output_df.drop(columns=['reasons'], inplace=True)
    
    # Save the output DataFrame to a CSV file
    output_csv_path = 'data/important_indicators.csv'
    output_df.to_csv(output_csv_path, index=False)
    print(f"Important indicators saved to {output_csv_path}")
    
    return output_df
