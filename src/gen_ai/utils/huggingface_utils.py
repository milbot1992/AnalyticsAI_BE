import os
from huggingface_hub import login
from transformers.agents import HfApiEngine, ReactCodeAgent

def initialise_hugging_face():
    """Initialise Hugging Face login and return the LLM engine and agent."""
    api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_token:
        raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable is not set.")
    
    login(api_token)

    # Initialise LLM engine
    llm_engine = HfApiEngine("meta-llama/Meta-Llama-3.1-70B-Instruct")

    # Initialise agent with allowed imports
    agent = ReactCodeAgent(
        tools=[],
        llm_engine=llm_engine,
        additional_authorized_imports=["numpy", "pandas", "matplotlib.pyplot", "seaborn", "jinja2", "tensorflow", "torch"],
        max_iterations=10,
    )
    return llm_engine, agent
