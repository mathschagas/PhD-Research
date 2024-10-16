import pandas as pd

def compare_csv_files(file1, file2):
    # Carregar os arquivos CSV
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
    except Exception as e:
        print(f"Erro ao carregar os arquivos: {e}")
        return
    
    # Verificar se as formas (shape) dos arquivos são iguais
    if df1.shape != df2.shape:
        print(f"Os arquivos têm tamanhos diferentes: {df1.shape} vs {df2.shape}")
        return False

    # Comparar o conteúdo dos arquivos
    comparison = df1.equals(df2)

    if comparison:
        print("Os arquivos CSV são idênticos.")
        return True
    else:
        print("Os arquivos CSV são diferentes.")
        # Exibe as diferenças linha por linha
        diff = df1.compare(df2)
        print("Diferenças encontradas:\n", diff)
        return False

if __name__ == "__main__":
    file1 = "simulation_results_15-09-2024_22-44-35.csv"  # Substitua pelo caminho do primeiro arquivo CSV
    file2 = "simulation_results_15-09-2024_22-47-04.csv"  # Substitua pelo caminho do segundo arquivo CSV

    compare_csv_files(file1, file2)
