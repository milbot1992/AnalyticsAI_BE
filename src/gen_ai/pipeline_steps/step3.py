import pandas as pd
import logging

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
        - rank: the rank of the local authority for this indicator compared to all of the others
        - Rank_Neighbour: the rank of the local authority compared to it's statistical neighbours
        - Lower CI 95.0 limit and Upper CI 95.0 limit: 95% confidence interval bounds for the measure
        - Neighbours: the value of the indicator for each of the similar neighbours
        - The indicators selected represent areas that are particularly relevant to local authority public health initiatives.
        - Commentary should explain why these indicators were chosen and why they may require intervention.
        """
  
    try:
        # Load the important indicators data
        df = pd.read_csv('data/comparison_with_neighbours.csv')

        # List to store Hugging Face commentary for each row
        commentary_list = []

        # Loop through each row of the dataframe and generate commentary for each indicator
        for _, row in df.iterrows():
            # Convert the row to a dictionary for submission to the agent
            row_data = row.to_dict()

            # Prepare the input prompt for the agent with the specified row of data
            prompt = f"""
            You are an expert data analyst. Please load the source file and analyse it's content.
            This source file identifies key performance indicators for a local authority. 
            Your goal is to provide a detailed analytical summary for each indicator, explaining 
            why it highlights poor performance for the local authority and why it has been flagged as important.

            Row data:
            {row_data}
            
            Instructions:
            1. For each indicator in the dataset, use the fields provided and turn them into an analytical summary.
            2. Use analytical knowledge like an expert data analyst would to return a sentence/paragraph that could appear
               in a statistical publication

            Output:
            For each indicator, return a summary

            Example:
            "Summary: The local authority is ranked 1st, indicating the lowest life expectancy 
            compared to the other authorities. The z_score of 2.5 shows the authority is significantly above the 
            national average, placing it well outside one standard deviation. This issue is further emphasised 
            by its Rank_Neighbour of 1, showing it performs worse than all its statistical neighbours.
            """

            # Running the agent with the prompt and additional notes
            result = agent.run(
                prompt,
                additional_notes=additional_notes,
            )
            commentary_list.append(result)

        # Add the Hugging Face commentary as a new column to the dataframe
        df['Hugging Face Commentary'] = commentary_list

        # Save the dataframe with the new commentary to a new CSV file
        output_file = 'data/output.csv'
        df.to_csv(output_file, index=False)
        logging.info(f"Output saved to {output_file}")
        return df

    except Exception as e:
        logging.error(f"Error in generating agent insight: {e}")
        return "Error: Unable to generate agent commentary."
