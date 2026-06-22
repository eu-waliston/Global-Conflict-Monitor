from scripts.extract_data import extract_data
from scripts.clean_data import clean_data
from scripts.load_mysql import load_mysql
from scripts.queries import run_all_queries
from scripts.generate_graphs import generate_all_graphs

from database.connection import (
    get_engine,
    get_server_engine
)
from scripts.generate_maps import generate_conflict_map

# 🧠 EXECUTAR SQL FILE


def execute_sql_file(file_path, engine):

    print(f'\n🧠 EXECUTANDO SQL: {file_path}')

    with open(file_path, 'r', encoding='utf-8') as file:
        sql_script = file.read()

    connection = engine.raw_connection()

    cursor = connection.cursor()

    sql_commands = sql_script.split(';')

    for command in sql_commands:

        command = command.strip()

        if command:

            cursor.execute(command)

    connection.commit()

    cursor.close()
    connection.close()

    print(f'✅ SQL EXECUTADO: {file_path}')

# 🚀 PIPELINE PRINCIPAL


def main():

    print('\n🌍 GLOBAL CONFLICT MONITOR')
    print('🚀 INICIANDO PIPELINE...\n')


    # 1️⃣ EXTRAÇÃO DOS DADOS


    print('\n📦 ETAPA 1 — EXTRAÇÃO DOS DADOS')

    conflicts_df, onesided_df = extract_data()


    # 2️⃣ LIMPEZA DOS DADOS


    print('\n🧹 ETAPA 2 — LIMPEZA DOS DADOS')

    cleaned_conflicts = clean_data(conflicts_df)


    # 3️⃣ CRIAR BANCO E TABELAS RAW


    print('\n🗄️ ETAPA 3 — CRIANDO BANCO RAW')

    # conexão sem database
    server_engine = get_server_engine()

    # cria database
    execute_sql_file(
        'sql/create_database.sql',
        server_engine
    )

    # conexão com database
    engine = get_engine()

    # cria tabela raw
    execute_sql_file(
        'sql/create_raw_table.sql',
        engine
    )


    # 4️⃣ ENVIAR DADOS PARA MYSQL


    print('\n📤 ETAPA 4 — ENVIANDO DADOS')

    load_mysql(cleaned_conflicts)


    # 5️⃣ NORMALIZAÇÃO


    print('\n🧠 ETAPA 5 — NORMALIZAÇÃO')

    execute_sql_file(
        'sql/create_normalized_tables.sql',
        engine
    )

    execute_sql_file(
        'sql/insert_normalized_data.sql',
        engine
    )


    # 6️⃣ CONSULTAS SQL


    print('\n📊 ETAPA 6 — CONSULTAS SQL')

    query_results = run_all_queries()


    # 7️⃣ GRÁFICOS


    print('\n📈 ETAPA 7 — GRÁFICOS')

    generate_all_graphs(query_results)

    generate_conflict_map()


    # FINALIZAÇÃO


    print('\n🎉 PIPELINE FINALIZADO COM SUCESSO!')
    print('\n✅ Banco populado')
    print('✅ Consultas executadas')
    print('✅ Gráficos gerados')
    print('✅ Projeto funcionando')



# ▶️ START


if __name__ == '__main__':

    main()