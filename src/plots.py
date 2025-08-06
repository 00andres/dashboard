import plotly.express as px

def plot_ventas_globales(df):
    ventas = df.groupby("Year")["Global_Sales"].sum().reset_index()
    plataforma_lider_por_año = df.groupby(["Year", "Platform"])["Global_Sales"].sum().reset_index()
    lider = plataforma_lider_por_año.loc[plataforma_lider_por_año.groupby("Year")["Global_Sales"].idxmax()]
    lider = lider.set_index("Year")["Platform"]
    ventas["Plataforma_Lider"] = ventas["Year"].map(lider)
    fig = px.line(
        ventas, x="Year", y="Global_Sales",
        markers=True,
        color_discrete_sequence=["#4CAF50"],
        title="Ventas globales a lo largo del tiempo",
        labels={"Global_Sales": "Ventas (millones)", "Year": "Año"},
        hover_data={"Global_Sales": ":.2f", "Plataforma_Lider": True, "Year": False}
    )
    fig.update_traces(
        mode="lines+markers",
        hovertemplate="<b>Año %{x}</b><br>Ventas: %{y:.2f} M<br>🎮 Plataforma líder: %{customdata[0]}"
    )
    fig.update_layout(hovermode="x unified")
    return fig

def plot_top_plataformas(df, ordenar_por="Global_Sales"):
    if ordenar_por == "Global_Sales":
        top = df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False).head(10)
    else:
        top = df.groupby("Platform")["Name"].count().sort_values(ascending=False).head(10)
    top_df = top.reset_index()
    fig = px.bar(
        top_df, x=ordenar_por if ordenar_por == "Global_Sales" else "Name", y="Platform",
        orientation="h",
        color=ordenar_por if ordenar_por == "Global_Sales" else "Name",
        color_continuous_scale="Viridis",
        title=f"Top 10 plataformas por {ordenar_por.lower().replace('_', ' ')}",
        labels={ordenar_por: "Ventas (millones)" if ordenar_por=="Global_Sales" else "Número de juegos", "Platform": "Plataforma", "Name": "Número de juegos"}
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    return fig

def plot_top_generos(df, ordenar_por="Global_Sales"):
    if ordenar_por == "Global_Sales":
        top = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)
    else:
        top = df.groupby("Genre")["Name"].count().sort_values(ascending=False)
    top_df = top.reset_index()
    fig = px.bar(
        top_df, x="Global_Sales" if ordenar_por=="Global_Sales" else "Name", y="Genre",
        orientation="h",
        color="Genre",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title=f"Ventas globales por género (ordenado por {ordenar_por.lower().replace('_', ' ')})",
        labels={"Global_Sales": "Ventas (millones)", "Genre": "Género", "Name": "Número de juegos"}
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    return fig

def plot_NA_vs_EU(df, regiones=["NA_Sales", "EU_Sales"]):
    top20 = df.sort_values(by="Global_Sales", ascending=False).head(20)
    fig = px.bar(
        top20,
        x="Name",
        y=regiones,
        barmode="stack",
        title="Ventas combinadas por región (Top 20 juegos)",
        labels={"value": "Ventas (millones)", "Name": "Juego", "variable": "Región"},
        color_discrete_map={
            "NA_Sales": "#e53935",
            "EU_Sales": "#1e88e5",
            "JP_Sales": "#fbc02d",
            "Other_Sales": "#00897b"
        }
    )
    fig.update_xaxes(tickangle=45)
    return fig
