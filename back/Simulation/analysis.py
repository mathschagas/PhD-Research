import pandas as pd
import ast
import os


def string_to_dict(string):
    """Converts a JSON-like string into a dictionary."""
    try:
        return ast.literal_eval(string)
    except (ValueError, SyntaxError):
        return {}


def flatten_dict(prefix, dictionary):
    """Flattens a nested dictionary, adding the prefix to the keys."""
    flattened = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            flattened.update(flatten_dict(f"{prefix}_{key}", value))
        else:
            flattened[f"{prefix}_{key}"] = value
    return flattened


def transform_csv(input_file, output_file, excluded_columns):
    """Transforms a CSV file by expanding dictionary columns into separate columns."""
    # Load the CSV into a DataFrame
    df = pd.read_csv(input_file)

    # Initialize an auxiliary DataFrame for the new columns
    expanded_data = pd.DataFrame()

    # Process specific columns
    for col in ['Best_Component_Info', 'cbr', 'raw_penalty']:
        if col in df.columns:
            expanded = df[col].apply(lambda x: flatten_dict("", string_to_dict(x)))
            expanded_df = pd.json_normalize(expanded)
            expanded_data = pd.concat([expanded_data, expanded_df], axis=1)

    # Drop excluded columns
    df = df.drop(columns=excluded_columns, errors='ignore')

    # Combine the original DataFrame with the expanded data
    df = pd.concat([df, expanded_data], axis=1)

    # Save the transformed DataFrame to a new CSV file
    df.to_csv(output_file, index=False)


def transform_all_csv_in_folder(folder_path, excluded_columns):
    """Processes all CSV files in a folder."""
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            input_file = os.path.join(folder_path, filename)
            output_file = os.path.join(folder_path, f'transformed_{filename}')
            try:
                print(f"Processing file: {filename}")
                transform_csv(input_file, output_file, excluded_columns)
            except Exception as e:
                print(f"Error processing {filename}: {e}")


# Configuration
EXCLUDED_COLUMNS = ['id', 'type', 'score', 'Best_Component_Info', 'Task_Info', 'Ranking_Info']

# Example usage
folder_path = 'results/u-cbr'
transform_all_csv_in_folder(folder_path, EXCLUDED_COLUMNS)
