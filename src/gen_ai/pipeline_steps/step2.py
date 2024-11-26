import os
import pandas as pd
import matplotlib.pyplot as plt

def generate_agent_insight(llm_engine, agent):
    """
    Generate statistical insight using Hugging Face agent for a specific row.

    Returns:
        str: Agent-generated commentary as a string.
    """

    # Additional notes to provide context for the agent
    additional_notes = """
        ### Variable Notes
        - Area Name: Name of the Local Authority (e.g., Manchester)
        - Area Code: Unique code for the Local Authority
        - Value: Measure of interest (e.g., life expectancy)
        - z_score: Standard score indicating how many standard deviations a value is from the mean
        - Lower CI 95.0 limit and Upper CI 95.0 limit: 95% confidence interval bounds for the measure
        - The indicators selected represent areas that are particularly relevant to local authority public health initiatives.
        - Commentary should explain why these indicators were chosen and why they may require intervention.
        """
  
    try:
        # Load the important indicators data
        df = pd.read_csv('data/important_indicators.csv')

        # List to store Hugging Face commentary for each row
        commentary_list = []

        # Loop through each row of the dataframe and generate commentary for each indicator
        for _, row in df.iterrows():
            # Prepare the input prompt for the agent with each row of data
            prompt = f"""
            You are an expert data analyst. Please analyze the following data for the local authority:

            Area Name: {row['Area Name']}
            Area Code: {row['Area Code']}
            Value: {row['Value']}
            z_score: {row['z_score']}
            Lower CI 95.0 limit: {row['Lower CI 95.0 limit']}
            Upper CI 95.0 limit: {row['Upper CI 95.0 limit']}

            Based on this information, explain why this indicator is important to focus on within local authority public health initiatives and why it may require intervention. 
            """

            # Running the agent with the prompt and additional notes
            result = agent.run(
                prompt,
                additional_notes=additional_notes,
                source_file="data/important_indicators.csv"
            )
            commentary_list.append(result)

        # Add the Hugging Face commentary as a new column to the dataframe
        df['Hugging Face Commentary'] = commentary_list

        # Save the dataframe with the new commentary to a new CSV file
        output_file = 'data/output.csv'
        df.to_csv(output_file, index=False)
        print(f"Output saved to {output_file}")
        return df

    except Exception as e:
        print(f"Error in generating agent insight: {e}")
        return "Error: Unable to generate agent commentary."