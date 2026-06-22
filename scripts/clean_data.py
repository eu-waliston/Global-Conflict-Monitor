import pandas as pd


def clean_data(conflicts_df):

    print('\n🧹 LIMPANDO DADOS...')

    # =================================================
    # COLUNAS NECESSÁRIAS
    # =================================================

    conflicts_clean = conflicts_df[[
        'conflict_id',
        'location',
        'region',
        'side_a',
        'side_b',
        'year',
        'type_of_conflict',
        'intensity_level',
        'incompatibility',
        'territory_name',
        'start_date'
    ]].copy()

    # =================================================
    # REMOVER NULOS IMPORTANTES
    # =================================================

    conflicts_clean = conflicts_clean.dropna(
        subset=['conflict_id', 'location']
    )

    # =================================================
    # PADRONIZAR NOMES
    # =================================================

    conflicts_clean.columns = [
        col.lower()
        for col in conflicts_clean.columns
    ]

    # =================================================
    # EXPORTAR CSV LIMPO
    # =================================================

    conflicts_clean.to_csv(
        'data/processed/conflicts_clean.csv',
        index=False
    )

    print('\n✅ CSV limpo criado com sucesso!')

    print(conflicts_clean.head())

    # =================================================
    # RETORNO
    # =================================================

    return conflicts_clean