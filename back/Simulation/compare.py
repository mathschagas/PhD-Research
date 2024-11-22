import pandas as pd

def load_csv_to_dataframe(file_path):
    return pd.read_csv(file_path)

def compare_dataframes(df1, df2):
    # Align the dataframes to ensure they have the same labels
    df1, df2 = df1.align(df2, join='outer', axis=0, fill_value=0)
    df1, df2 = df1.align(df2, join='outer', axis=1, fill_value=0)
    comparison_result = df1.compare(df2)
    return comparison_result

def convert_to_numeric(df):
    return df.apply(pd.to_numeric, errors='coerce').fillna(0)

def calculate_absolute_difference(df1, df2):
    # Align the dataframes to ensure they have the same labels
    df1, df2 = df1.align(df2, join='outer', axis=0, fill_value=0)
    df1, df2 = df1.align(df2, join='outer', axis=1, fill_value=0)
    # Convert dataframes to numeric
    df1 = convert_to_numeric(df1)
    df2 = convert_to_numeric(df2)
    absolute_difference = (df1 - df2).abs()
    return absolute_difference

def main():
    # Load the transformed CSVs into dataframes
    df1 = load_csv_to_dataframe('results/cbru_results_22-11-2024_03-50-08/transformed_2ConstraintsLikert.csv')
    df2 = load_csv_to_dataframe('results/random_results_22-11-2024_07-54-53/transformed_2ConstraintsLikert.csv')
    # Compare the dataframes
    comparison_result = compare_dataframes(df1, df2)
    # Save the comparison result to a CSV file
    comparison_result.to_csv('results/comparison_result.csv')
    
    # Calculate the absolute difference between the dataframes
    absolute_difference = calculate_absolute_difference(df1, df2)
    # Save the absolute difference to a CSV file
    absolute_difference.to_csv('results/absolute_difference.csv')

if __name__ == "__main__":
    main()
