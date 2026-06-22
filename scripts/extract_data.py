import pandas as pd

def extract_data():
    # Ler arquivos Excel
    conflicts_df = pd.read_excel(
        'data/raw/UcdpPrioConflict_v25_1.xlsx'
    )

    onesided_df = pd.read_excel(
        'data/raw/OneSided_v25_1.xlsx'
    )

    print('Conflitos:', conflicts_df.shape)
    print('Violência Unilateral:', onesided_df.shape)

    # Mostrar colunas
    print ('=== COLUNAS CONFLICTS')
    print(conflicts_df.columns)

    print('=== COLUNAS DE ONESIDED')
    print(onesided_df.columns)

    return conflicts_df, onesided_df
