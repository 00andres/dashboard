import streamlit as st
from load_data import cargar_datos
from plots import plot_ventas_globales, plot_top_plataformas, plot_top_generos, plot_NA_vs_EU

st.set_page_config(page_title="Storytelling de Videojuegos", layout="wide")

st.title("🎮 El Viaje de las Ventas de Videojuegos")
st.markdown("""
En el mundo gamer, las ventas cuentan historias fascinantes:  
**¿Qué consolas lideraron? ¿Qué géneros dominaron el mercado?**  
Este dashboard explora la evolución del mercado desde los clásicos hasta la revolución online.
""")

# Carga datos
df = cargar_datos()

# --- FILTROS ---

platforms = st.sidebar.multiselect(
    "🕹️ Plataforma", sorted(df["Platform"].unique()), default=sorted(df["Platform"].unique())
)
years = st.sidebar.slider(
    "📅 Rango de años", int(df["Year"].min()), int(df["Year"].max()), (int(df["Year"].min()), int(df["Year"].max()))
)
genres = st.sidebar.multiselect(
    "🎭 Género", sorted(df["Genre"].unique()), default=sorted(df["Genre"].unique())
)

# Filtrado
df_filtrado = df[
    (df["Platform"].isin(platforms)) &
    (df["Genre"].isin(genres)) &
    (df["Year"] >= years[0]) &
    (df["Year"] <= years[1])
]

st.info(f"🔎 Analizando **{len(df_filtrado)}** registros filtrados entre **{years[0]}** y **{years[1]}**.")

# --- OPCIONES DE INTERACCIÓN ---
st.sidebar.markdown("## Opciones de visualización")

# Selección de gráficos
graficos_disponibles = {
    "Ventas globales a lo largo del tiempo": "ventas_globales",
    "Top 10 plataformas": "top_plataformas",
    "Ventas por género": "top_generos",
    "Ventas combinadas NA vs EU (Top 20 juegos)": "ventas_regiones"
}
graficos_seleccionados = st.sidebar.multiselect(
    "Selecciona gráficos a mostrar", list(graficos_disponibles.keys()),
    default=list(graficos_disponibles.keys())
)

# Orden para top plataformas y géneros
orden_plataformas = st.sidebar.radio(
    "Orden Top Plataformas por:", ("Global_Sales", "Número de juegos")
)
orden_generos = st.sidebar.radio(
    "Orden Ventas por Género por:", ("Global_Sales", "Número de juegos")
)

# Filtro para regiones en gráfico NA vs EU
regiones_disponibles = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
regiones_seleccionadas = st.sidebar.multiselect(
    "Selecciona regiones para gráfico de ventas por región (Top 20 juegos):",
    regiones_disponibles,
    default=["NA_Sales", "EU_Sales"]
)

# --- SECCIONES DEL DASHBOARD ---

st.header("❓ Problema")
st.markdown("""
Las tendencias de ventas de videojuegos no siempre son claras. Surgen preguntas:  
- ¿Cuándo crecieron más?  
- ¿Qué plataformas son realmente líderes?  
""")

st.header("🧪 Análisis Interactivo")

if "Ventas globales a lo largo del tiempo" in graficos_seleccionados:
    st.subheader("📈 Ventas globales a lo largo del tiempo")
    st.markdown("""
    Este gráfico muestra la suma total de ventas globales de videojuegos por año.  
    La línea conecta las ventas anuales, y al pasar el cursor sobre cada punto, se revela la plataforma líder de ese año.  
    Esto permite observar tendencias, picos y caídas en el mercado global y el impacto de distintas plataformas a lo largo del tiempo.
    """)
    st.plotly_chart(plot_ventas_globales(df_filtrado), use_container_width=True)

if "Top 10 plataformas" in graficos_seleccionados:
    st.subheader("🏆 Top 10 plataformas")
    st.markdown(f"""
    Aquí se muestra un ranking de las 10 plataformas con mayores ventas o mayor número de juegos, según la opción seleccionada: **{orden_plataformas}**.  
    Esto ayuda a identificar cuáles consolas han sido más exitosas comercialmente o en producción de títulos.
    """)
    st.plotly_chart(plot_top_plataformas(df_filtrado, ordenar_por=orden_plataformas), use_container_width=True)

if "Ventas por género" in graficos_seleccionados:
    st.subheader("🎮 Ventas por género")
    st.markdown(f"""
    Este gráfico presenta las ventas totales o cantidad de juegos por género (por ejemplo, Acción, Deportes, Aventura).  
    El orden es según: **{orden_generos}**.  
    Permite identificar qué tipos de juegos son más populares y generan más ingresos.
    """)
    st.plotly_chart(plot_top_generos(df_filtrado, ordenar_por=orden_generos), use_container_width=True)

if "Ventas combinadas NA vs EU (Top 20 juegos)" in graficos_seleccionados:
    st.subheader("🌍 Ventas combinadas por región (Top 20 juegos)")
    st.markdown(f"""
    Visualiza las ventas apiladas por regiones seleccionadas para los 20 juegos más vendidos.  
    Las regiones seleccionadas son: **{', '.join(regiones_seleccionadas)}**.  
    Esto permite comparar el éxito comercial de un juego en distintos mercados geográficos y ver cómo varía su popularidad por región.
    """)
    st.plotly_chart(plot_NA_vs_EU(df_filtrado, regiones=regiones_seleccionadas), use_container_width=True)

st.header("✅ Conclusión y propuesta")
st.markdown("""
Este análisis muestra claramente:  
- El impacto de plataformas icónicas como PS2 o Wii.  
- La relevancia de géneros deportivos y de acción.  
- La dominancia de Norteamérica en muchas franquicias.

👉 **Propuesta**: usar estos datos para planificar futuros lanzamientos priorizando plataformas y géneros con tendencia creciente.
""")


