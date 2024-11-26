import argparse
import logging
import pandas as pd
from src.utils.fetch_data import fetch_indicator_data
from src.analysis.enrich_data import calculate_statistics
from src.gen_ai.openai_integration import generate_gpt_commentary
from src.gen_ai.huggingface_pipeline import hugging_face_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_and_process_data(indicator_ids):
    """Fetch data and process it."""
    logging.info("Fetching indicator data...")
    return fetch_indicator_data(indicator_ids)

def calculate_and_save_statistics():
    """Calculate and save statistical metrics."""
    logging.info("Calculating statistics...")
    return calculate_statistics()

def generate_commentary_for_local_authority():
    """Generate GPT commentary for local authority."""
    logging.info("Generating GPT commentary...")
    return generate_gpt_commentary()

def analyze_with_hugging_face(local_authority, area_code):
    """Analyze data using Hugging Face model."""
    logging.info(f"Analyzing data for {local_authority} with Hugging Face...")
    return hugging_face_pipeline(local_authority, area_code)

def save_processed_data(data, filename):
    """Save processed data to CSV."""
    logging.info(f"Saving processed data to {filename}...")
    data.to_csv(filename, index=False)

def main():
    # Parse command-line arguments for flexibility
    parser = argparse.ArgumentParser(description="Process public health data.")
    parser.add_argument("--fetch", action="store_true", help="Fetch indicator data")
    parser.add_argument("--stats", action="store_true", help="Calculate and save statistics")
    parser.add_argument("--gpt", action="store_true", help="Generate GPT commentary")
    parser.add_argument("--huggingface", action="store_true", help="Run Hugging Face analysis")
    parser.add_argument("--save", action="store_true", help="Save processed data")
    parser.add_argument("--local_authority", type=str, default="Hartlepool", help="Local Authority for Hugging Face analysis")
    parser.add_argument("--area_code", type=str, default="E06000001", help="Area code for Hugging Face analysis")
    
    args = parser.parse_args()

    indicator_ids = [40501, 90366, 90362, 93562, 92901, 93505, 91102, 93523, 93190]
    
    # Step-wise conditional execution based on arguments
    if args.fetch:
        combined_data = fetch_and_process_data(indicator_ids)
    
    if args.stats:
        stats_data = calculate_and_save_statistics()

    if args.gpt:
        data_with_commentary = generate_commentary_for_local_authority()
    
    if args.huggingface:
        data_with_all_commentary = analyze_with_hugging_face(args.local_authority, args.area_code)
    
    if args.save:
        if args.huggingface:
            save_processed_data(data_with_all_commentary, 'data/processed_data.csv')
        elif args.gpt:
            save_processed_data(data_with_commentary, 'data/gpt_processed_data.csv')

if __name__ == "__main__":
    main()
