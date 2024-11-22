import pandas as pd

def load_csv_to_dataframe(file_path):
    return pd.read_csv(file_path)

def compare_dataframes(df1, df2):
    # Align the dataframes to ensure they have the same labels
    df1, df2 = df1.align(df2, join='outer', axis=0, fill_value=0)
    df1, df2 = df1.align(df2, join='outer', axis=1, fill_value=0)
    comparison_result = df1.compare(df2)
    return comparison_result

def calculate_absolute_difference(df1, df2):
    # Align the dataframes to ensure they have the same labels
    df1, df2 = df1.align(df2, join='outer', axis=0, fill_value=0)
    df1, df2 = df1.align(df2, join='outer', axis=1, fill_value=0)
    absolute_difference = (df1 - df2).abs()
    return absolute_difference

def main():
    # Load the transformed CSVs into dataframes
    df1 = load_csv_to_dataframe('results/cbru_results_21-11-2024_17-41-46/transformed_1ConstraintBin.csv')
    df2 = load_csv_to_dataframe('results/random_results_21-11-2024_17-56-23/1ConstraintBin.csv')
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
