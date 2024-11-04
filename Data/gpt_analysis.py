import os
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GPT_API_KEY"),
)

def get_gpt_analysis(row):
    prompt = (
        f"I want you to act as a Statistician. I will provide you with details related with statistics. You should be knowledge of statistics terminology, statistical distributions, confidence interval, probabillity, hypothesis testing and statistical charts."
        f"Analyse the measure for Local Authority {row['Area Name']} (code: {row['Area Code']}). "
        f"Return only the key insights, no more than 150 words."
        f"Return any Indicator Values 1 decimal place, any z_scores to 2 decimal places and any percentages to 0 decimal place."
        f"Give the analysis of the measure for the Local Authority in bullet points with the most relevant first. Followed by a short overall summary sentence"
        f"Return the bullets in the style of a research paper / publication - very succinct and highlighting the things that these papers tend to highlight about data."
        f"E.g. Overall, Middlesbrough has a higher Under 75 mortality rate from cancer compared to other Local Authorities, indicating potential health concerns or disparities that may need further investigation."
        f"When speaking about the indicator use the indicator name rather than 'indicator'"
        f"The value of {row['Indicator Name']} is {row['Value']}, with a z-score of {row['z_score']:.2f}. "
        f"This measure has a 95% confidence interval from {row['Lower CI 95.0 limit']} to {row['Upper CI 95.0 limit']} "
        f"and a 99.8% confidence interval from {row['Lower CI 99.8 limit']} to {row['Upper CI 99.8 limit']}. "
        f"The confidence interval width for 95% is {row['CI_95_width']:.2f} and for 99.8% is {row['CI_99.8_width']:.2f}. "
    )
    
    # Include national comparison if available
    if 'comparison_to_england' in row:
        prompt += f"This Local Authority is considered {row['Compared to England value or percentiles']} compared to the national average. "
    
    # Add standard deviation context
    if row['within_1_std']:
        prompt += "The value falls within one standard deviation of the mean, indicating it is close to the average. "
    elif row['within_2_std']:
        prompt += "The value is within two standard deviations, suggesting it is somewhat uncommon but not an extreme outlier. "
    else:
        prompt += "The value is more than two standard deviations away from the mean, making it a significant outlier. "
    
    prompt += "Provide a brief analysis on how this Local Authority compares to others and any insights based on these statistics."

    # API call to GPT
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    # Convert the response to JSON format and parse it
    json_response = response.to_json()
    response_dict = json.loads(json_response)

    # Access the content of the message
    content_message = response_dict["choices"][0]["message"]["content"]
    print('content: ', content_message)

    return content_message

def generate_gpt_commentary(data):
    data['gpt_commentary'] = data.apply(get_gpt_analysis, axis=1)
    return data
