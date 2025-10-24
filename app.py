import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson
import copy
import plotly.express as px
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Champions League Burbuja",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNCIONES DEL MODELO (Las que ya creamos) ---

# Cargar datos de equipos
@st.cache_data
def cargar_datos_equipos():
    datos_equipos = {
        "Paris S-G": {"xG_avg": 7.9 / 3, "xGA_avg": 4.1 / 3}, "Bayern Munich": {"xG_avg": 10.8 / 3, "xGA_avg": 1.4 / 3},
        "Inter": {"xG_avg": 9.8 / 3, "xGA_avg": 2.3 / 3}, "Arsenal": {"xG_avg": 6.3 / 3, "xGA_avg": 1.5 / 3},
        "Real Madrid": {"xG_avg": 9.8 / 3, "xGA_avg": 2.0 / 3}, "Dortmund": {"xG_avg": 4.3 / 3, "xGA_avg": 3.7 / 3},
        "Manchester City": {"xG_avg": 5.0 / 3, "xGA_avg": 2.8 / 3}, "Newcastle Utd": {"xG_avg": 6.5 / 3, "xGA_avg": 2.3 / 3},
        "Barcelona": {"xG_avg": 5.0 / 3, "xGA_avg": 3.9 / 3}, "Liverpool": {"xG_avg": 7.6 / 3, "xGA_avg": 2.5 / 3},
        "Chelsea": {"xG_avg": 5.0 / 3, "xGA_avg": 4.1 / 3}, "Sporting CP": {"xG_avg": 6.1 / 3, "xGA_avg": 2.1 / 3},
        "Qarabağ": {"xG_avg": 4.0 / 3, "xGA_avg": 5.8 / 3}, "Galatasaray": {"xG_avg": 6.6 / 3, "xGA_avg": 4.1 / 3},
        "Tottenham": {"xG_avg": 2.8 / 3, "xGA_avg": 5.4 / 3}, "PSV Eindhoven": {"xG_avg": 5.5 / 3, "xGA_avg": 5.9 / 3},
        "Atalanta": {"xG_avg": 5.6 / 3, "xGA_avg": 5.1 / 3}, "Marseille": {"xG_avg": 2.4 / 3, "xGA_avg": 5.5 / 3},
        "Atlético Madrid": {"xG_avg": 5.5 / 3, "xGA_avg": 5.4 / 3}, "Club Brugge": {"xG_avg": 4.2 / 3, "xGA_avg": 8.2 / 3},
        "Athletic Club": {"xG_avg": 4.7 / 3, "xGA_avg": 3.1 / 3}, "Eint Frankfurt": {"xG_avg": 2.0 / 3, "xGA_avg": 8.6 / 3},
        "Napoli": {"xG_avg": 2.2 / 3, "xGA_avg": 6.2 / 3}, "Union SG": {"xG_avg": 4.8 / 3, "xGA_avg": 9.5 / 3},
        "Juventus": {"xG_avg": 4.2 / 3, "xGA_avg": 5.9 / 3}, "Bodø/Glimt": {"xG_avg": 6.5 / 3, "xGA_avg": 9.2 / 3},
        "Monaco": {"xG_avg": 5.4 / 3, "xGA_avg": 5.4 / 3}, "Slavia Prague": {"xG_avg": 4.9 / 3, "xGA_avg": 9.3 / 3},
        "Pafos FC": {"xG_avg": 2.4 / 3, "xGA_avg": 7.3 / 3}, "Leverkusen": {"xG_avg": 5.2 / 3, "xGA_avg": 5.2 / 3},
        "Villarreal": {"xG_avg": 3.4 / 3, "xGA_avg": 3.3 / 3}, "FC Copenhagen": {"xG_avg": 3.7 / 3, "xGA_avg": 4.7 / 3},
        "Olympiacos": {"xG_avg": 3.0 / 3, "xGA_avg": 5.7 / 3}, "Qaırat Almaty": {"xG_avg": 2.3 / 3, "xGA_avg": 8.9 / 3},
        "Benfica": {"xG_avg": 2.6 / 3, "xGA_avg": 4.8 / 3}, "Ajax": {"xG_avg": 3.1 / 3, "xGA_avg": 6.0 / 3}
    }
    return datos_equipos

@st.cache_data
def cargar_partidos_y_tabla():
    # ... (Aquí irían las funciones inicializar_tabla y la lista partidos_filtrados)
    # Para mantenerlo corto, las incluyo dentro de la función principal de simulación.
    # En un proyecto real, las tendrías separadas como aquí.
    pass

def simular_partido(equipo_local, equipo_visitante, datos_equipos):
    stats_local = datos_equipos[equipo_local]
    stats_visitante = datos_equipos[equipo_visitante]
    home_advantage = 0.15
    lambda_local = (stats_local["xG_avg"] + stats_visitante["xGA_avg"] + home_advantage) / 2
    lambda_visitante = (stats_visitante["xG_avg"] + stats_local["xGA_avg"]) / 2
    goles_local = poisson.rvs(mu=lambda_local, size=1)[0]
    goles_visitante = poisson.rvs(mu=lambda_visitante, size=1)[0]
    return (goles_local, goles_visitante)

def correr_simulacion(num_simulaciones, datos_equipos):
    # Cargar datos estáticos
    partidos_restantes = [ ("Benfica", "Bayern Munich"), ("Bodø/Glimt", "Real Madrid"), ("Qarabağ", "Dortmund"), ("Galatasaray", "Slavia Prague"), ("Sporting CP", "Club Brugge"), ("Juventus", "Union SG"), ("Paris S-G", "PSV Eindhoven"), ("Atalanta", "Leverkusen"), ("Liverpool", "Real Madrid"), ("Barcelona", "Monaco"), ("Atalanta", "Juventus"), ("Bayern Munich", "Barcelona"), ("Benfica", "Liverpool"), ("Dortmund", "Bodø/Glimt"), ("Galatasaray", "Qarabağ"), ("Club Brugge", "Sporting CP"), ("PSV Eindhoven", "Paris S-G"), ("Leverkusen", "Atalanta"), ("Real Madrid", "Benfica"), ("Liverpool", "Bayern Munich"), ("Monaco", "Barcelona"), ("Juventus", "Atalanta"), ("Bayern Munich", "Real Madrid"), ("Benfica", "Dortmund"), ("Bodø/Glimt", "Qarabağ"), ("Galatasaray", "Slavia Prague"), ("Club Brugge", "Juventus"), ("Sporting CP", "PSV Eindhoven"), ("Paris S-G", "Atalanta"), ("Leverkusen", "Club Brugge"), ("Real Madrid", "Bayern Munich"), ("Dortmund", "Benfica"), ("Qarabağ", "Bodø/Glimt"), ("Slavia Prague", "Galatasaray") ]
    equipos_validos = list(datos_equipos.keys())
    partidos_filtrados = [ (local, visitante) for local, visitante in partidos_restantes if local in equipos_validos and visitante in equipos_validos ]
    
    tabla_inicial = { "Paris S-G": {"pts": 9, "gf": 13, "ga": 3}, "Bayern Munich": {"pts": 9, "gf": 12, "ga": 2}, "Inter": {"pts": 9, "gf": 9, "ga": 0}, "Arsenal": {"pts": 9, "gf": 8, "ga": 0}, "Real Madrid": {"pts": 9, "gf": 8, "ga": 1}, "Dortmund": {"pts": 7, "gf": 12, "ga": 7}, "Manchester City": {"pts": 7, "gf": 6, "ga": 2}, "Newcastle Utd": {"pts": 6, "gf": 8, "ga": 2}, "Barcelona": {"pts": 6, "gf": 9, "ga": 4}, "Liverpool": {"pts": 6, "gf": 8, "ga": 4}, "Chelsea": {"pts": 6, "gf": 7, "ga": 4}, "Sporting CP": {"pts": 6, "gf": 7, "ga": 4}, "Qarabağ": {"pts": 6, "gf": 6, "ga": 5}, "Galatasaray": {"pts": 6, "gf": 5, "ga": 6}, "Tottenham": {"pts": 5, "gf": 3, "ga": 2}, "PSV Eindhoven": {"pts": 4, "gf": 8, "ga": 6}, "Atalanta": {"pts": 4, "gf": 2, "ga": 5}, "Marseille": {"pts": 3, "gf": 6, "ga": 4}, "Atlético Madrid": {"pts": 3, "gf": 7, "ga": 8}, "Club Brugge": {"pts": 3, "gf": 5, "ga": 7}, "Athletic Club": {"pts": 3, "gf": 4, "ga": 7}, "Eint Frankfurt": {"pts": 3, "gf": 7, "ga": 11}, "Napoli": {"pts": 3, "gf": 4, "ga": 9}, "Union SG": {"pts": 3, "gf": 3, "ga": 9}, "Juventus": {"pts": 2, "gf": 6, "ga": 7}, "Bodø/Glimt": {"pts": 2, "gf": 5, "ga": 7}, "Monaco": {"pts": 2, "gf": 3, "ga": 6}, "Slavia Prague": {"pts": 2, "gf": 2, "ga": 5}, "Pafos FC": {"pts": 2, "gf": 1, "ga": 5}, "Leverkusen": {"pts": 2, "gf": 5, "ga": 10}, "Villarreal": {"pts": 1, "gf": 2, "ga": 5}, "FC Copenhagen": {"pts": 1, "gf": 4, "ga": 8}, "Olympiacos": {"pts": 1, "gf": 1, "ga": 8}, "Qaırat Almaty": {"pts": 1, "gf": 1, "ga": 9}, "Benfica": {"pts": 0, "gf": 2, "ga": 7}, "Ajax": {"pts": 0, "gf": 1, "ga": 11} }
    for equipo in tabla_inicial: tabla_inicial[equipo]['gd'] = tabla_inicial[equipo]['gf'] - tabla_inicial[equipo]['ga']

    # Bucle de simulación
    resultados_finales = []
    for i in range(num_simulaciones):
        tabla_simulacion = copy.deepcopy(tabla_inicial)
        for local, visitante in partidos_filtrados:
            goles_local, goles_visitante = simular_partido(local, visitante, datos_equipos)
            tabla_simulacion[local]['gf'] += goles_local; tabla_simulacion[local]['ga'] += goles_visitante; tabla_simulacion[local]['gd'] = tabla_simulacion[local]['gf'] - tabla_simulacion[local]['ga']
            tabla_simulacion[visitante]['gf'] += goles_visitante; tabla_simulacion[visitante]['ga'] += goles_local; tabla_simulacion[visitante]['gd'] = tabla_simulacion[visitante]['gf'] - tabla_simulacion[visitante]['ga']
            if goles_local > goles_visitante: tabla_simulacion[local]['pts'] += 3
            elif goles_visitante > goles_local: tabla_simulacion[visitante]['pts'] += 3
            else: tabla_simulacion[local]['pts'] += 1; tabla_simulacion[visitante]['pts'] += 1
        tabla_final_ordenada = sorted(tabla_simulacion.items(), key=lambda item: (item[1]['pts'], item[1]['gd'], item[1]['gf']), reverse=True)
        resultados_finales.append([equipo[0] for equipo in tabla_final_ordenada])
    
    # Análisis de probabilidades
    conteo_posiciones = {equipo: {'Top8': 0, 'Playoff': 0, 'Eliminado': 0} for equipo in datos_equipos.keys()}
    for ranking in resultados_finales:
        for posicion, equipo in enumerate(ranking):
            if posicion < 8: conteo_posiciones[equipo]['Top8'] += 1
            elif posicion < 24: conteo_posiciones[equipo]['Playoff'] += 1
            else: conteo_posiciones[equipo]['Eliminado'] += 1
    
    lista_probabilidades = []
    for equipo, conteos in conteo_posiciones.items():
        prob_top8 = (conteos['Top8'] / num_simulaciones) * 100
        prob_playoff = (conteos['Playoff'] / num_simulaciones) * 100
        prob_eliminado = (conteos['Eliminado'] / num_simulaciones) * 100
        lista_probabilidades.append({'Equipo': equipo, 'Prob Top 8 (%)': round(prob_top8, 2), 'Prob Playoff (%)': round(prob_playoff, 2), 'Prob Eliminado (%)': round(prob_eliminado, 2)})
    
    df_probabilidades = pd.DataFrame(lista_probabilidades).sort_values(by='Prob Top 8 (%)', ascending=False).reset_index(drop=True)
    return df_probabilidades


# --- INTERFAZ DE STREAMLIT ---

st.title("⚽ Modelo de la Burbuja - UEFA Champions League")
st.markdown("Explora las probabilidades de clasificación a Octavos de Final, Playoffs o Eliminación basadas en una simulación de Montecarlo de 10,000 escenarios posibles.")

st.sidebar.header("⚙️ Configuración de la Simulación")

# Slider para el número de simulaciones
num_simulaciones = st.sidebar.slider(
    "Número de simulaciones a ejecutar:",
    min_value=100,
    max_value=20000,
    value=10000,
    step=100,
    help="Un número mayor de simulaciones da resultados más precisos, pero tarda más en calcular."
)

# Botón para ejecutar la simulación
if st.sidebar.button("🚀 Ejecutar Simulación"):
    with st.spinner(f'Ejecutando {num_simulaciones} simulaciones... Esto puede tardar un momento.'):
        datos = cargar_datos_equipos()
        df_resultados = correr_simulacion(num_simulaciones, datos)
        st.session_state.df_resultados = df_resultados
        st.success("¡Simulación completada!")

# Comprobar si los resultados existen en el estado de la sesión
if 'df_resultados' not in st.session_state:
    st.warning("Por favor, ejecuta la simulación usando el botón en la barra lateral para ver los resultados.")
else:
    df_resultados = st.session_state.df_resultados

    st.header("📊 Ranking de Probabilidades de Clasificación")
    
    st.markdown("### Probabilidad de Clasificación Directa a Octavos (Top 8)")
    top_8 = df_resultados[['Equipo', 'Prob Top 8 (%)']].head(8)
    fig_top8 = px.bar(top_8, x='Prob Top 8 (%)', y='Equipo', orientation='h', color='Prob Top 8 (%)', color_continuous_scale='viridis')
    fig_top8.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_top8, use_container_width=True)

    st.markdown("### Análisis de la 'Burbuja' (Puestos 9-24 actuales)")
    equipos_burbuja = df_resultados.iloc[8:24]
    fig_burbuja = px.bar(
        equipos_burbuja,
        x='Equipo',
        y=['Prob Top 8 (%)', 'Prob Playoff (%)', 'Prob Eliminado (%)'],
        labels={'value': 'Probabilidad (%)', 'variable': 'Destino Final'},
        title="Distribución de Probabilidades para Equipos de la Burbuja"
    )
    st.plotly_chart(fig_burbuja, use_container_width=True)

    st.markdown("### Tabla Completa de Probabilidades")
    st.dataframe(df_resultados, use_container_width=True)

    st.markdown("---")
    st.markdown("**Metodología:**")
    st.markdown("""
    - **Modelo Predictivo:** Se utiliza una distribución de Poisson para simular el resultado de cada partido restante.
    - **Variables Clave:** El modelo se basa en los promedios de Goles Esperados (xG) y Goles Esperados En Contra (xGA) de cada equipo.
    - **Simulación:** Se ejecuta el resto de la temporada `N` veces (definido por el usuario) para generar una distribución de resultados finales.
    - **Cálculo de Probabilidades:** Las probabilidades se calculan como el porcentaje de veces que un equipo acaba en cada rango de clasificación (Top 8, Playoff, Eliminado) a lo largo de todas las simulaciones.
    """)
