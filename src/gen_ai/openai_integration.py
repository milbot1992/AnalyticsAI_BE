import os
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import json

load_dotenv()

# Initialise the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("GPT_API_KEY"))

def generate_statistical_insight(row):
    """
    Generate a detailed statistical analysis prompt for GPT based on row data.

    Parameters:
        row (pd.Series): A row of data with statistical details for a specific Local Authority.

    Returns:
        str: The GPT-generated analysis as a string.
    """
    # Prompt tailored to statistical analysis
    prompt = (
        f"I want you to act as a Statistician. I will provide you with details related with statistics."
        f"You should be knowledge of statistics terminology, statistical distributions, confidence interval," 
        f"probabillity, hypothesis testing and statistical charts."
        f"Analyse the measure for Local Authority {row['Area Name']} (code: {row['Area Code']})."
        f"Return only the key insights, no more than 150 words."
        f"Return any Indicator Values 1 decimal place, any z_scores to 2 decimal places and any percentages to 0 decimal place."
        f"Give the analysis of the measure for the Local Authority in bullet points with the most relevant first. Followed by a short overall summary sentence"
        f"Return the bullets in the style of a research paper / publication - very succinct and highlighting the things that these papers tend to highlight about data."
        f"E.g. Overall, Middlesbrough has a higher {row['Indicator Name']} compared to other Local Authorities, indicating X."
        f"When speaking about the indicator use the indicator name rather than 'indicator'"
        f"The value of {row['Indicator Name']} is {row['Value']}, with a z-score of {row['z_score']:.2f}. "
        f"This measure has a 95% confidence interval from {row['Lower CI 95.0 limit']} to {row['Upper CI 95.0 limit']} "
    )
    
    # Add national comparison context if available
    if 'comparison_to_england' in row:
        prompt += f"This Local Authority is considered {row['Compared to England value or percentiles']} compared to the national average. "
    
    # Include standard deviation context for clarity on deviation from the mean
    if row['within_1_std']:
        prompt += "The value falls within one standard deviation of the mean, indicating it is close to the average. "
    elif row['within_2_std']:
        prompt += "The value is within two standard deviations, suggesting it is somewhat uncommon but not an extreme outlier. "
    else:
        prompt += "The value is more than two standard deviations away from the mean, making it a significant outlier. "
    
    prompt += "Provide a brief analysis on how this Local Authority compares to others and any insights based on these statistics."

    # API call to GPT
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        # Convert the response to JSON format and parse it
        json_response = response.to_json()
        response_dict = json.loads(json_response)

        # Access the content of the message
        content_message = response_dict["choices"][0]["message"]["content"]

        # Return the content from GPT's response
        return content_message

    except Exception as e:
        print(f"Error in API call: {e}")
        return "Error: Unable to generate analysis."

def generate_gpt_commentary():
    """
    Read data from a CSV file, apply GPT-generated statistical analysis to each row in the DataFrame.

    Parameters:
        data (pd.DataFrame): DataFrame containing data with required statistical details.

    Returns:
        pd.DataFrame: Original DataFrame with an additional 'gpt_commentary' column.
    """
    
    # Load data from the CSV file
    input_file = 'data/analysed_data.csv'
    data = pd.read_csv(input_file)

    # Apply statistical insights to generate GPT commentary
    data['gpt_commentary'] = data.apply(generate_statistical_insight, axis=1)

    # Save the updated data back to the CSV
    output_file = 'data/analysed_data.csv'
    data.to_csv(output_file, index=False)
    print(f"Data with GPT commentary saved to {output_file}")

    return data
