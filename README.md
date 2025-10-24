# Champions-league-bubble-mode
⚽ Modelo de la Burbuja - UEFA Champions League

Un dashboard interactivo que utiliza simulación de Montecarlo y modelos predictivos para analizar las probabilidades de clasificación de los equipos en la fase de grupos de la UEFA Champions League. ¿Quiénes están en la "burbuja" y qué destino les espera?
## 🧠 ¿Cómo Funciona?

El proyecto se basa en una metodología robusta de análisis de datos:

1.  **Modelo Predictivo de Partidos**: Se utiliza la **distribución de Poisson** para simular el resultado de cada uno de los partidos restantes. La tasa de goles esperada (`lambda`) para cada equipo se calcula en base a sus promedios de **Goles Esperados (xG)** y **Goles Esperados en Contra (xGA)**.

2.  **Simulación de Montecarlo**: El motor predictivo se ejecuta en un bucle de **10,000 iteraciones**. En cada iteración, se simula el resto de la temporada, actualizando una tabla de posiciones.
3.  
3.  **Análisis de Probabilidades**: Al finalizar las 10,000 simulaciones, se analiza en cuántas ocasiones cada equipo acabó en cada rango de clasificación (Top 8, Playoff o Eliminado) para calcular sus probabilidades finales.

## 🚀 Cómo Ejecutar el Proyecto Localmente
## 🛠️ Tecnologías Utilizadas

-   **Python**: Lenguaje principal.
-   **Streamlit**: Para la creación del dashboard interactivo.
-   **Pandas**: Para la manipulación y análisis de datos.
-   **NumPy & SciPy**: Para los cálculos numéricos y la simulación de Poisson.
-   **Plotly**: Para la creación de gráficos interactivos.
-   **Git & GitHub**: Para el control de versiones y el alojamiento del código.
-   ## 📈 Hallazgos Clave

El modelo revela insights fascinantes sobre la nueva fase de grupos:

> **Ejemplo de Insight**: "El Atalanta, a pesar de estar en la posición 17 tras 3 jornadas, tiene una probabilidad de **[X.X]%** de clasificarse directamente a Octavos de Final, superando a equipos que actualmente están por encima de ellos en la tabla."

*(Este es un gran lugar para añadir 1 o 2 de tus conclusiones más impactantes del análisis).*
