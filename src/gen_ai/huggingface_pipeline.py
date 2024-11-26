from transformers.agents import HfApiEngine, ReactCodeAgent
from huggingface_hub import login
import os
import pandas as pd
import matplotlib.pyplot as plt
from src.gen_ai.pipeline_steps.step1 import find_important_indicators
from src.gen_ai.pipeline_steps.step2 import generate_agent_insight

def initialize_hugging_face():
    """Initialize Hugging Face login and return the LLM engine and agent."""
    api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_token:
        raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable is not set.")
    
    login(api_token)

    # Initialize LLM engine
    llm_engine = HfApiEngine("meta-llama/Meta-Llama-3.1-70B-Instruct")

    # Initialize agent with allowed imports
    agent = ReactCodeAgent(
        tools=[],
        llm_engine=llm_engine,
        additional_authorized_imports=["numpy", "pandas", "matplotlib.pyplot", "seaborn", "jinja2", "tensorflow", "torch"],
        max_iterations=10,
    )
    return llm_engine, agent

def hugging_face_pipeline(local_authority, area_code):
    """
    Main pipeline function to analyze indicators for a specific local authority.

    Parameters:
        local_authority (str): The name of the local authority to analyze.
        area_code (str): The unique code for the local authority.
    """
    try:
        # Initialize Hugging Face components
        llm_engine, agent = initialize_hugging_face()
        
        # Find and display the important indicators
        important_indicators = find_important_indicators(local_authority, area_code)
        
        # Get Hugging Face insights into important indicators
        agent_insights = generate_agent_insight(llm_engine, agent)
        
    except ValueError as ve:
        print(f"Initialization Error: {ve}")
    except Exception as e:
        print(f"Pipeline Error: {e}")


