import pandas as pd

from database.connection import get_engine
engine = get_engine()

def conflicts_by_year():

    print('\n📊 CONSULTA: ConflITOS POR ANO')

    query = '''
    SELECT
        year,
        COUNT(*) AS total_conflicts

    FROM conflicts

    GROUP BY year

    ORDER BY year
    '''

    df = pd.read_sql(query, engine)

    print(df.head())

    return df

def high_fatality_conflicts():

    print('\n🔥 CONSULTA: CONFLITOS MAIS MORTAIS')

    query = '''
    SELECT
        conflict_name,
        intensity_level

    FROM conflicts

    WHERE conflict_id IN
    (
        SELECT conflict_id
        FROM fatalities
        WHERE deaths_best > 10000
    )
    '''

    df = pd.read_sql(query, engine)

    print(df.head())

    return df

def actor_conflicts():

    print('\n🌍 CONSULTA: ATORES DOS CONFLITOS')

    query = '''
    SELECT
        conflicts.conflict_name,
        actors.actor_name,
        fatalities.deaths_best

    FROM conflicts

    JOIN conflict_actors
        ON conflicts.conflict_id =
        conflict_actors.conflict_id

    JOIN actors
        ON conflict_actors.actor_id =
        actors.actor_id

    JOIN fatalities
        ON conflicts.conflict_id =
        fatalities.conflict_id

    ORDER BY fatalities.deaths_best DESC
    '''

    df = pd.read_sql(query, engine)

    print(df.head())

    return df

def regions_and_conflicts():

    print('\n☠️ CONSULTA: REGIÕES E CONFLITOS')

    query = '''
    SELECT
        regions.region_name,
        conflicts.conflict_name

    FROM regions

    LEFT JOIN countries
        ON regions.region_id =
        countries.region_id

    LEFT JOIN conflicts
        ON countries.country_id =
        conflicts.country_id
    '''

    df = pd.read_sql(query, engine)

    print(df.head())

    return df

def all_actors_union():

    print('\n🌍 CONSULTA: UNION DE ATORES')

    query = """

    SELECT side_a AS actor_name
    FROM global_conflict_raw

    UNION

    SELECT side_b AS actor_name
    FROM global_conflict_raw

    """

    df = pd.read_sql(query, engine)

    print(df.head())

    return df
def top_conflict_countries():

    print('\n📈 CONSULTA: PAÍSES COM MAIS CONFLITOS')

    query = '''
    SELECT
        countries.country_name,
        COUNT(*) AS total_conflicts

    FROM conflicts

    JOIN countries
        ON conflicts.country_id =
        countries.country_id

    GROUP BY countries.country_name

    ORDER BY total_conflicts DESC

    LIMIT 10
    '''

    df = pd.read_sql(query, engine)

    print(df.head())

    return df

def fatalities_by_year():

    print('\n🌍 CONSULTA: FATALIDADES POR ANO')

    query = """

    SELECT

        c.year,

        SUM(f.deaths_best) AS total_deaths

    FROM fatalities f

    JOIN conflicts c
    ON f.conflict_id = c.conflict_id

    GROUP BY c.year

    ORDER BY c.year

    """

    df = pd.read_sql(query, engine)

    print(df.head())

    return df
def conflicts_by_type():

    print('\n⚔️ CONSULTA: TIPOS DE CONFLITO')

    query = '''
    SELECT
        conflict_types.type_name,
        COUNT(*) AS total

    FROM conflicts

    JOIN conflict_types
        ON conflicts.type_id =
        conflict_types.type_id

    GROUP BY conflict_types.type_name

    ORDER BY total DESC
    '''

    df = pd.read_sql(query, engine)

    print(df.head())

    return df


# =====================================================
# 🧠 EXECUTAR TODAS CONSULTAS
# =====================================================

def run_all_queries():

    print('\n🧠 EXECUTANDO TODAS AS CONSULTAS...')

    results = {
        'conflicts_by_year': conflicts_by_year(),
        'high_fatality_conflicts': high_fatality_conflicts(),
        'actor_conflicts': actor_conflicts(),
        'regions_and_conflicts': regions_and_conflicts(),
        'all_actors_union': all_actors_union(),
        'top_conflict_countries': top_conflict_countries(),
        'fatalities_by_year': fatalities_by_year(),
        'conflicts_by_type': conflicts_by_type()
    }

    print('\n✅ TODAS AS CONSULTAS EXECUTADAS!')

    return results

if __name__ == '__main__':

    run_all_queries()