import pandas as pd
import folium

from folium.plugins import (
    HeatMap,
    MarkerCluster
)

from database.connection import get_engine

engine = get_engine()


def generate_conflict_map():

    print('\n🌍 GERANDO MAPA INTERATIVO AVANÇADO...')

    # =========================================================
    # CONSULTA SQL COMPLETA
    # =========================================================

    query = """

    SELECT

        c.country_name AS location,

        cf.year,

        cf.side_a,

        cf.side_b,

        cf.intensity_level,

        ct.type_name,

        f.deaths_best

    FROM conflicts cf

    JOIN countries c
        ON cf.country_id = c.country_id

    LEFT JOIN conflict_types ct
        ON cf.type_id = ct.type_id

    LEFT JOIN fatalities f
        ON cf.conflict_id = f.conflict_id

    WHERE c.country_name IS NOT NULL

    """

    df = pd.read_sql(query, engine)

    print(df.head())

    # =========================================================
    # MAPA DARK MODE
    # =========================================================

    world_map = folium.Map(

        location=[20, 0],

        zoom_start=2,

        tiles='CartoDB dark_matter'

    )

    # =========================================================
    # CLUSTER DE MARCADORES
    # =========================================================

    marker_cluster = MarkerCluster().add_to(world_map)

    # =========================================================
    # COORDENADAS MANUAIS
    # =========================================================

    coordinates = {

        'India': [20.5937, 78.9629],
        'Israel': [31.0461, 34.8516],
        'Egypt': [26.8206, 30.8025],
        'Afghanistan': [33.9391, 67.7100],
        'Iraq': [33.2232, 43.6793],
        'Syria': [34.8021, 38.9968],
        'Ukraine': [48.3794, 31.1656],
        'Russia': [61.5240, 105.3188],
        'Sudan': [12.8628, 30.2176],
        'Somalia': [5.1521, 46.1996],
        'Pakistan': [30.3753, 69.3451],
        'Nigeria': [9.0820, 8.6753],
        'Yemen': [15.5527, 48.5164],
        'Libya': [26.3351, 17.2283],
        'Turkey': [38.9637, 35.2433],
        'Iran': [32.4279, 53.6880],
        'Colombia': [4.5709, -74.2973],
        'Myanmar': [21.9162, 95.9560],
        'China': [35.8617, 104.1954],
        'Ethiopia': [9.1450, 40.4897]

    }

    # =========================================================
    # HEATMAP DATA
    # =========================================================

    heat_data = []

    # =========================================================
    # CONTADORES
    # =========================================================

    total_conflicts = len(df)

    total_countries = df['location'].nunique()

    total_deaths = df['deaths_best'].fillna(0).sum()

    print(f'\n🌍 TOTAL CONFLITOS: {total_conflicts}')
    print(f'🌎 TOTAL PAÍSES: {total_countries}')
    print(f'☠️ TOTAL MORTES: {int(total_deaths)}')

    # =========================================================
    # LOOP DOS CONFLITOS
    # =========================================================

    for _, row in df.iterrows():

        country = row['location']

        if country not in coordinates:
            continue

        lat, lon = coordinates[country]

        # =====================================================
        # INTENSIDADE
        # =====================================================

        try:
            intensity = int(row['intensity_level'])
        except:
            intensity = 1

        # =====================================================
        # CORES POR INTENSIDADE
        # =====================================================

        if intensity == 1:
            color = 'yellow'

        elif intensity == 2:
            color = 'orange'

        else:
            color = 'red'

        # =====================================================
        # MORTES
        # =====================================================

        deaths = row['deaths_best']

        if pd.isna(deaths):
            deaths = 0

        # =====================================================
        # TAMANHO DO MARCADOR
        # =====================================================

        radius = max(4, min(deaths / 1000, 25))

        # =====================================================
        # POPUP COMPLETO
        # =====================================================

        popup_text = f"""

        <div style="width:300px">

        <h3>🌍 Global Conflict Monitor</h3>

        <hr>

        <b>Country:</b> {country}<br>

        <b>Year:</b> {row['year']}<br>

        <b>Side A:</b> {row['side_a']}<br>

        <b>Side B:</b> {row['side_b']}<br>

        <b>Intensity:</b> {intensity}<br>

        <b>Conflict Type:</b> {row['type_name']}<br>

        <b>Estimated Deaths:</b> {int(deaths)}<br>

        </div>

        """

        # =====================================================
        # CIRCLE MARKER
        # =====================================================

        folium.CircleMarker(

            location=[lat, lon],

            radius=radius,

            popup=folium.Popup(
                popup_text,
                max_width=350
            ),

            color=color,

            fill=True,

            fill_color=color,

            fill_opacity=0.7

        ).add_to(marker_cluster)

        # =====================================================
        # HEATMAP
        # =====================================================

        heat_data.append([lat, lon, intensity])

    # =========================================================
    # ADICIONAR HEATMAP
    # =========================================================

    HeatMap(

        heat_data,

        radius=18,

        blur=12

    ).add_to(world_map)

    # =========================================================
    # LEGENDA HTML
    # =========================================================

    legend_html = """

    <div style="
    position: fixed;
    bottom: 40px;
    left: 40px;
    width: 260px;
    height: 180px;
    background-color: white;
    z-index:9999;
    font-size:14px;
    border-radius:10px;
    padding:15px;
    box-shadow:0 0 15px rgba(0,0,0,0.5);
    ">

    <h4>🌍 Conflict Intensity</h4>

    <p>
    🟡 Low Intensity<br>
    🟠 Medium Intensity<br>
    🔴 High Intensity
    </p>

    <hr>

    <p>
    ☠️ Marker size = deaths<br>
    🔥 Heatmap = concentration
    </p>

    </div>

    """

    world_map.get_root().html.add_child(
        folium.Element(legend_html)
    )

    # =========================================================
    # EXPORTAR HTML
    # =========================================================

    world_map.save(
        'graphs/conflict_map.html'
    )

    print('\n✅ MAPA INTERATIVO GERADO!')
    print('📍 Arquivo: graphs/conflict_map.html')