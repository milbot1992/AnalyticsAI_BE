from transformers.agents import HfApiEngine, ReactCodeAgent
from huggingface_hub import login
import os
import pandas as pd
import matplotlib.pyplot as plt

from src.gen_ai.pipeline_steps.step1 import find_important_indicators
from src.gen_ai.pipeline_steps.step2 import compared_to_neighbours
from src.gen_ai.pipeline_steps.step3 import generate_agent_insight
from src.gen_ai.utils.huggingface_utils import initialise_hugging_face

def hugging_face_pipeline(local_authority, area_code):
    """
    Main pipeline function to analyze indicators for a specific local authority.

    Parameters:
        local_authority (str): The name of the local authority to analyze.
        area_code (str): The unique code for the local authority.
    """
    try:
        # Initialise Hugging Face components
        llm_engine, agent = initialise_hugging_face()
        
        # Find and display the important indicators
        # important_indicators = find_important_indicators(local_authority, area_code)

        # Compare area to the nearest statistical neighbours
        neighbour_comparison = compared_to_neighbours(local_authority, area_code)
        
        # Get Hugging Face insights into important indicators
        agent_insights = generate_agent_insight(llm_engine, agent)
        
    except ValueError as ve:
        print(f"Initialization Error: {ve}")
    except Exception as e:
        print(f"Pipeline Error: {e}")


