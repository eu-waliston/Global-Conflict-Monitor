import pandas as pd
import matplotlib.pyplot as plt

from database.connection import get_engine
engine = get_engine()

def generate_all_graphs(query_results):

    # Consulta SQL
    query = '''
    SELECT year, COUNT(*) AS total
    FROM conflicts
    GROUP BY year
    ORDER BY year
    '''

    # DataFrame

    df = pd.read_sql(query, engine)

    # Grafico
    plt.figure(figsize=(12,5))

    plt.plot(df['year'], df['total'])

    plt.title('Quantidade de conflitos por ano')
    plt.xlabel('Ano')
    plt.ylabel('Total de Conflitos')

    plt.savefig('graphs/conflicts_by_year.png')

    plt.show()
    print('Gráfico gerado com sucesso!')