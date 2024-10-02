# imports
import pandas as pd  # Importa la biblioteca pandas para el manejo de datos en forma de DataFrame
import numpy as np  # Importa la biblioteca numpy para operaciones matemáticas y de matrices
import plotly.express as px  # Importa Plotly Express para crear visualizaciones interactivas
import os  # Proporciona funciones para interactuar con el sistema operativo
import plotly.io as pio  # Módulo de I/O de Plotly para configurar el estilo de las visualizaciones
import statsmodels.api as sm  # Biblioteca para realizar análisis estadísticos avanzados
import re  # Biblioteca para trabajar con expresiones regulares, útil para extraer datos de textos

# Configuración de la plantilla de visualización predeterminada de Plotly
pio.templates.default = "plotly"

"""
Este script de Python genera las tablas y figuras para el artículo basado en GPT.
"""


def produce_tables_figures(dg_results,datatitle):
    """
    Esta función produce las tablas y figuras de los resultados del experimento
    del Juego del Dictador, utilizado en el estudio de Brookins y DeBacker.

    Args:
        dg_results (pandas.DataFrame): DataFrame que contiene los resultados del Juego del Dictador
        datatitle (str): título del modelo GPT utilizado para generar los resultados (ej. "GPT-3.5" o "GPT-4")

    Returns:
        None (las imágenes y archivos de texto se guardan en disco)
    """

    # Asignamos el DataFrame de resultados a una variable local
    df = dg_results
    
    # Mantener solo las primeras 500 observaciones del DataFrame.
    # Nota: Debido a interrupciones en el modelo, hay un total de 501 observaciones.
    df = df[:500]
    
    # Buscar la asignación en la respuesta generada por el modelo GPT
    # Utiliza una expresión regular para extraer los dígitos (0-9) de la columna 'GPTResponse'
    df.loc[:, "Allocation"] = (
        df["GPTResponse"].str.extract(r'(\d)',expand=False).astype(float)
    )

    # Reemplazar los valores de "50" por "5" en la columna Allocation para normalizar respuestas 50-50
    df["Allocation"].replace(
        {50: 5}, inplace=True
    )  # para los casos que la división haya sido 50-50


    # Imprimir el DataFrame para ver la estructura y verificar el procesamiento
    print(df)

    
    # Figura 1: Distribución de las asignaciones en el experimento con el modelo GPT
    fig = px.histogram(
        df, x="Allocation", nbins=10, range_x=[0, 10], histnorm="density",opacity=0.75,title=datatitle, text_auto=True
    )

    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1), 
        font=dict(family="Times New Roman", size=14, color="Black"), # Fuente y estilo del gráfico
        yaxis_title="Frequency", # Etiqueta para el eje y
        bargap=0.2, # Espacio entre las barras
        bargroupgap=0.1 # Espacio entre grupos de barras
    )
    
   # Añadir una línea vertical en la media de las asignaciones
    fig.add_vline(
        x=df.Allocation.mean(),  # La posición de la línea es la media de la columna "Allocation"
        line_width=5,  # Grosor de la línea
        line_dash="dash",  # Estilo de línea punteada
        line_color="black"  # Color negro para la línea
    )

    # Mostrar la figura generada
    fig.show()

# Leer los resultados del archivo Excel
dg_results_35 = pd.read_excel(
    os.path.join("..", "EXCEL FINAL MODELOS", "dictator_game_log_35_turbo.xlsx")
)

# Llamar a la función para generar las tablas y figuras
produce_tables_figures(dg_results_35, "dictator_game_log_35_turbo")
