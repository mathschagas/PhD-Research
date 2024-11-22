import pandas as pd
import os

def convert_csv_to_xlsx(csv_file_path, xlsx_file_path):
    # Lê o arquivo CSV
    df = pd.read_csv(csv_file_path)
    # Cria um objeto ExcelWriter
    with pd.ExcelWriter(xlsx_file_path) as writer:
        # Itera sobre os tipos de incerteza únicos
        for uncertainty_type in df['Uncertainty_Type'].unique():
            # Filtra o DataFrame pelo tipo de incerteza
            df_filtered = df[df['Uncertainty_Type'] == uncertainty_type].drop(columns=['Uncertainty_Type'])
            # Escreve o DataFrame filtrado em uma nova aba
            df_filtered.to_excel(writer, sheet_name=str(uncertainty_type), index=False)

def convert_all_csv_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(directory_path, filename)
            xlsx_file_path = os.path.splitext(csv_file_path)[0] + '.xlsx'
            convert_csv_to_xlsx(csv_file_path, xlsx_file_path)

# Exemplo de uso
if __name__ == "__main__":
    directory_path = 'results'
    convert_all_csv_in_directory(directory_path)
