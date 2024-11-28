import pandas as pd

def compared_to_neighbours(local_authority, area_code):
    """
    Compare important indicators of a local authority with its statistical neighbours.

    Args:
        local_authority (str): Name of the local authority.
        area_code (str): Area code of the local authority.

    Returns:
        pd.DataFrame: A DataFrame showing the comparison of important indicators with neighbours.
    """
    # Load the important indicators data
    df_indicators = pd.read_csv('data/important_indicators.csv')

    # Load the statistical neighbours data
    df_neighbours = pd.read_csv('data/5peers.csv')

    # Load the complete dataset
    df_complete = pd.read_csv('data/analysed_data.csv')

    # Filter the important indicators for the given local authority
    important_indicators = df_indicators[
        (df_indicators['Area Name'] == local_authority) & 
        (df_indicators['Area Code'] == area_code)
    ]

    # Get the peers of the local authority
    peers = df_neighbours.loc[df_neighbours['UTLA22NM'] == local_authority].iloc[0, 1:].tolist()

    # Placeholder for output data
    results = []

    # Define the ranking order for each indicator
    ranking_order = {
        40501: False,  # Descending rank (higher values rank 1)
        90366: True,   # Ascending rank (lower values rank 1)
        90362: True,
        93562: True,
        92901: False,
        93505: True,
        91102: True,
        93523: True,
        93190: False,
    }

    # Rank to sentence mapping
    rank_sentence_mapping = {
        1: "local authority is ranked the poorest compared to its statistical neighbours",
        2: "local authority is ranked the second poorest compared to its statistical neighbours",
        3: "local authority is ranked the third poorest compared to its statistical neighbours",
        4: "local authority is ranked the fourth poorest compared to its statistical neighbours",
        5: "local authority is ranked the second best compared to its statistical neighbours",
        6: "local authority is ranked the best compared to its statistical neighbours",
    }

    # Iterate through important indicators
    for _, row in important_indicators.iterrows():
        indicator_id = row['Indicator ID']
        indicator_name = row['Indicator Name']
        local_value = row['Value']
        
        # Collect neighbour values for the same indicator
        neighbour_values = []
        for peer in peers:
            peer_row = df_complete[
                (df_complete['Area Name'] == peer) & 
                (df_complete['Indicator ID'] == indicator_id)
            ]
            if not peer_row.empty:
                neighbour_values.append(peer_row.iloc[0]['Value'])
            else:
                neighbour_values.append(None)  # If no data for the peer, add None
        
        # Include the local authority's value for ranking
        all_values = [local_value] + [v for v in neighbour_values if v is not None]
        
        # Sort values based on the ranking order
        ascending = ranking_order.get(indicator_id, True)  # Default to ascending if not specified
        ranked_values = sorted(all_values, reverse=not ascending)
        
        # Determine the rank of the local authority
        local_rank = ranked_values.index(local_value) + 1

        # Get the rank sentence
        rank_sentence = rank_sentence_mapping.get(local_rank, f"rank is {local_rank}")
        
        # Construct the output row
        result = {
            **row.to_dict(),
            **{f"Neighbour{i+1}": (neighbour_values[i] if i < len(neighbour_values) else None) for i in range(5)},  # Handle missing neighbours
            "Rank_Neighbour": local_rank,
            "Rank_Neighbour_Sentence": rank_sentence,
        }
        results.append(result)

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Save the output DataFrame to a CSV file
    output_path = 'data/comparison_with_neighbours.csv'
    results_df.to_csv(output_path, index=False)
    print(f"Comparison with neighbours saved to {output_path}")

    return results_df
