import pandas as pd

def cargar_datos(ruta="data/vgsales.csv"):
    """
    Carga y limpia el dataset de videojuegos.
    Fuente: Kaggle Video Game Sales Dataset
    """
    df = pd.read_csv(ruta)
    df.dropna(inplace=True)
    df["Year"] = df["Year"].astype(int)
    return df
