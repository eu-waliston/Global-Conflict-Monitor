from database.connection import get_engine


def load_mysql(cleaned_conflicts):

    print('\n📤 ENVIANDO DADOS PARA MYSQL...')

    engine = get_engine()

    # Inserir no banco
    cleaned_conflicts.to_sql(
        'global_conflict_raw',
        con=engine,
        if_exists='append',
        index=False,
    )

    print('✅ Dados enviados para o MySQL!')