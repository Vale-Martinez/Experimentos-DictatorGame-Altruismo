# imports
import pandas as pd
import numpy as np
import plotly.express as px
import os
import plotly.io as pio
import statsmodels.api as sm
import re
from scipy.stats import chi2_contingency
from scipy import stats

# Establece el tema por defecto para las gráficas de Plotly
pio.templates.default = "plotly"

"""
Este script de Python genera las tablas y figuras para el artículo de GPT.
"""


def produce_stadistics(dg_4, dg_4turbo, dg_4o, dg_4omini, dg_35turbo):
 
    # Procesamos datos del modelo GPT-4
    df_4 = dg_4
    # Mantener solo las primeras 500 observaciones
    # Nota que debido a interrupciones del modelo, hay 501 observaciones en total
    df_4 = df_4[:500]
    # Encuentra la asignación (Allocation) en la respuesta del modelo
    df_4.loc[:, "Allocation"] = (
        df_4["GPTResponse"].str.extract(r'(\d)', expand=False).astype(float)
    )

    # Reemplazar valores de 50 con 5, ya que el modelo se refiere a un reparto 50-50
    df_4["Allocation"].replace({50: 5}, inplace=True)

    # Procesamos datos del modelo GPT-4 Turbo
    df_4turbo = dg_4turbo
    # Mantener solo las primeras 500 observaciones
    df_4turbo = df_4turbo[:500]
    # Encuentra la asignación en la respuesta del modelo
    df_4turbo.loc[:, "Allocation"] = (
        df_4turbo["GPTResponse"].str.extract(r'(\d)', expand=False).astype(float)
    )

    # Reemplazar valores de 50 con 5, para los casos que mencionan división 50-50
    df_4turbo["Allocation"].replace({50: 5}, inplace=True)

    # Procesamos datos del modelo GPT-4o
    df_4o = dg_4o
    # Mantener solo las primeras 500 observaciones
    df_4o = df_4o[:500]
    # Encuentra la asignación en la respuesta del modelo
    df_4o.loc[:, "Allocation"] = (
        df_4o["GPTResponse"].str.extract(r'(\d)', expand=False).astype(float)
    )

    df_4o["Allocation"].replace(
        {50: 5}, inplace=True
    )  # for these cases, it's saying split 50-50
   

    # Reemplazar valores de 50 con 5
    df_4o["Allocation"].replace({50: 5}, inplace=True)

    # Procesamos datos del modelo GPT-4o-mini
    df_4omini = dg_4omini
    # Mantener solo las primeras 500 observaciones
    df_4omini = df_4omini[:500]
    # Encuentra la asignación en la respuesta del modelo
    df_4omini.loc[:, "Allocation"] = (
        df_4omini["GPTResponse"].str.extract(r'(\d)', expand=False).astype(float)
    )

    # Reemplazar valores de 50 con 5
    df_4omini["Allocation"].replace({50: 5}, inplace=True)

    # Procesamos datos del modelo GPT-3.5 Turbo
    df_35turbo = dg_35turbo
    # Mantener solo las primeras 500 observaciones
    df_35turbo = df_35turbo[:500]
    # Encuentra la asignación en la respuesta del modelo
    df_35turbo.loc[:, "Allocation"] = (
        df_35turbo["GPTResponse"].str.extract(r'(\d)', expand=False).astype(float)
    )

    # Reemplazar valores de 50 con 5
    df_35turbo["Allocation"].replace({50: 5}, inplace=True)

    # Crear DataFrame con los resultados de cada modelo GPT
    df_resultadosGPT = pd.DataFrame({
        "gpt_4": df_4["Allocation"],
        "gpt_4turbo": df_4turbo["Allocation"],
        "gpt_4o": df_4o["Allocation"],
        "gpt_4omini": df_4omini["Allocation"],
        "gpt_35turbo": df_35turbo["Allocation"]
    })

   
    # Crear el gráfico tipo violin plot para visualizar las distribuciones
    fig = px.violin(df_resultadosGPT, title="Box Plot de Resultados de GPT", 
                    labels={'value': 'Allocation', 'variable': 'Model'}, template="presentation")

    # Mostrar el gráfico
    fig.show()

    # Mostrar estadísticas descriptivas de los resultados
    print(df_resultadosGPT.describe())
    

    # Crear histograma con los resultados de los experimentos
    fig = px.histogram(
        df_resultadosGPT,
        x=["gpt_4", "gpt_4turbo", "gpt_4o", "gpt_4omini", "gpt_35turbo"],
        histnorm="density",
        barmode="group",
        range_x=[0, 10],
        text_auto=True,
        opacity=0.75,
        title="Comparación de resultados de experimentos sobre modelos GPT",
        template="presentation"
    )

    # Personalizar el layout del histograma
    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        yaxis_title="Frecuencia",
        xaxis_title="Asignación",
        bargap=0.2,
        bargroupgap=0.1,
        legend_title="Modelos GPT"
    )
    fig.show()

    # Figura data por engle 
    # Datos del metaanálisis de Engel (2011)
    engel_data = {
         "One Shot Studies": {
            "Allocation": [
                0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1.0,
            ],
            "Fraction": [
                0.3133,
                0.0794,
                0.0934,
                0.0922,
                0.078,
                0.2127,
                0.0304,
                0.0142,
                0.0092,
                0.0064,
                0.0702,
            ],
        },
    }
    
    # Convertir los datos a un DataFrame
    df_engel = pd.DataFrame(engel_data["One Shot Studies"])

    # Calcular la media ponderada de Engel
    engel_mean = df_engel["Allocation"].dot(df_engel["Fraction"])

    # Crear gráfico de barras con los datos de Engel
    fig = px.bar(df_engel, x="Allocation", y="Fraction", 
                 title="Representación de resultados Meta-estudio Engel (2011) contra medias modelo GPT",
                 template="presentation")

    # Personalizar el layout
    fig.update_layout(
        yaxis_range=[0, 0.4],
        xaxis=dict(tickmode="linear", tick0=0, dtick=0.1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        legend_title="Medias por modelos GPT"
    )

    # Añadir líneas verticales para la media de Engel y de cada modelo GPT
    fig.add_vline(
        x=engel_mean, line_width=3, line_dash="dash", line_color="firebrick",  name="Media Meta-estudio Engle (2011) = " + str(engel_mean),showlegend=True,
    )

    fig.add_vline(
        x=df_resultadosGPT.gpt_35turbo.mean() / 10,
        line_width=3,
        line_dash="dash",
        line_color="black",
        name="Media GPT-3.5-turbo = "+ str (df_resultadosGPT.gpt_35turbo.mean() / 10),
        showlegend=True,
    )
     
    fig.add_vline(
        x=df_resultadosGPT.gpt_4turbo.mean() / 10,
        line_width=3,
        line_dash="dash",
        line_color="orange",
        name="Media GPT-4-turbo = "+ str (df_resultadosGPT.gpt_4turbo.mean() / 10),
        showlegend=True,
    )
    fig.add_vline(
        x=df_resultadosGPT.gpt_4.mean() / 10,
        line_width=3,
        line_dash="dash",
        line_color="green",
        name="Media GPT-4= "+ str (df_resultadosGPT.gpt_4.mean() / 10),
        showlegend=True,
    )
    fig.add_vline(
        x=df_resultadosGPT.gpt_4o.mean() / 10,
        line_width=3,
        line_dash="dash",
        line_color="magenta",
        name="Media GPT-4o = "+ str (df_resultadosGPT.gpt_4o.mean() / 10),
        showlegend=True,
    )
    fig.add_vline(
        x=df_resultadosGPT.gpt_4omini.mean() / 10,
        line_width=3,
        line_dash="dash",
        line_color="goldenrod",
        name="Media GPT-4omini = "+ str (df_resultadosGPT.gpt_4omini.mean() / 10),
        showlegend=True,
    )

    # Mostrar el gráfico
    fig.show()

    # Mostrar estadísticas descriptivas de los datos de Engel
    print(df_engel.describe())


    # Figuras para analisis anova
    # Crear el histograma para análisis individual del modelo GP4
    fig = px.histogram(
        df_resultadosGPT, x="gpt_4", nbins=10, range_x=[0, 10], histnorm="probability",opacity=0.75,title="Resultados de Modelo GPT-4",template= "presentation",
        text_auto=True)

    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        yaxis_title="Frequency",
        bargap=0.2,
        bargroupgap=0.1
    )
    fig.show()
    

    # Crear el histograma para análisis individual del modelo GP4-turbo
    fig = px.histogram(
        df_resultadosGPT, x="gpt_4turbo", nbins=10, range_x=[0, 10], histnorm="probability",opacity=0.75,title="Resultados de Modelo GPT-4-turbo",template= "presentation",
        text_auto=True)

    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        yaxis_title="Frequency",
        bargap=0.2,
        bargroupgap=0.1
    )
    fig.show()

    # Crear el histograma para análisis individual del modelo GP4o
    fig = px.histogram(
        df_resultadosGPT, x="gpt_4o", nbins=10, range_x=[0, 10], histnorm="probability",opacity=0.75,title="Resultados de Modelo GPT-4o",template= "presentation",
        text_auto=True)

    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        yaxis_title="Frequency",
        bargap=0.2,
        bargroupgap=0.1
    )
    fig.show()

    # Crear el histograma para análisis individual del modelo GP4o-mini
    fig = px.histogram(
        df_resultadosGPT, x="gpt_4omini", nbins=10, range_x=[0, 10], histnorm="probability",opacity=0.75,title="Resultados de Modelo GPT-4o-mini",template= "presentation",
        text_auto=True)

    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        yaxis_title="Frequency",
        bargap=0.2,
        bargroupgap=0.1
    )
    fig.show()

    # Crear el histograma para análisis individual del modelo GP3.5
    fig = px.histogram(
        df_resultadosGPT, x="gpt_35turbo", nbins=10, range_x=[0, 10], histnorm="probability",opacity=0.75,title="Resultados de Modelo GPT-3.5-turbo",template= "presentation",
        text_auto=True)

    fig.update_layout(
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        font=dict(family="Times New Roman", size=14, color="Black"),
        yaxis_title="Frequency",
        bargap=0.2,
        bargroupgap=0.1
    )
    fig.show()

    # Crear un gráfico de barras usando los datos de Engel (2011)
    fig = px.bar(df_engel, x="Allocation", y="Fraction", 
                 title="Representación de resultados Meta-estudio Engel (2011) contra medias modelo GPT", 
                 template="presentation")

    # Actualizar el layout del gráfico
    fig.update_layout(
        # Configurar el eje x para tener ticks lineales con un intervalo de 1
        xaxis=dict(tickmode="linear", tick0=0, dtick=1),
        
        # Definir la fuente de texto con Times New Roman, tamaño 14 y color negro
        font=dict(family="Times New Roman", size=14, color="Black"),
        
        # Etiqueta del eje y
        yaxis_title="Frequency",
        
        # Definir el espacio entre barras y entre grupos de barras
        bargap=0.2,         # Espacio entre barras individuales
        bargroupgap=0.1     # Espacio entre grupos de barras
    )

    # Mostrar el gráfico
    fig.show()
    
    #print (tabla_contingencia)

    #tabla_contingencia = pd.crosstab(df_4["Allocation"], df_4turbo["Allocation"],df_4o["Allocation"], df_4omini["Allocation"])
##
##    print("\n GPT4-GPT4turbo")
##    tabla_contingencia = pd.crosstab(df_resultadosGPT["gpt_4"], df_resultadosGPT["gpt_4turbo"])
##    chi2_stat, p_val, dof, ex = chi2_contingency(tabla_contingencia)
##    resta =( df_resultadosGPT["gpt_4"].std())** 2 - (df_resultadosGPT["gpt_4turbo"].std())** 2
##    resultado= np.sqrt(resta)
##    print(f"Diferencia de distribuciones : {resultado}")
##    print(f"Estadístico de Chi-cuadrado: {chi2_stat}")
##    print(f"Valor p: {p_val}")
##    print("-------------------------------------------------------------")
##
##    print("\n GPT4-GPT4o")
##    tabla_contingencia = pd.crosstab(df_resultadosGPT["gpt_4"], df_resultadosGPT["gpt_4o"])
##    chi2_stat, p_val, dof, ex = chi2_contingency(tabla_contingencia)
##    resta =( df_resultadosGPT["gpt_4"].std())** 2 - (df_resultadosGPT["gpt_4o"].std())** 2
##    resultado= np.sqrt(resta)
##    print(f"Diferencia de distribuciones : {resultado}")
##    print(f"Estadístico de Chi-cuadrado: {chi2_stat}")
##    print(f"Valor p: {p_val}")
##    print("-------------------------------------------------------------")
##
##    print("\n GPT4-GPT4omini")
##    tabla_contingencia = pd.crosstab(df_resultadosGPT["gpt_4"], df_resultadosGPT["gpt_4omini"])
##    chi2_stat, p_val, dof, ex = chi2_contingency(tabla_contingencia)
##    resta =( df_resultadosGPT["gpt_4"].std())** 2 - (df_resultadosGPT["gpt_4omini"].std())** 2
##    resultado= np.sqrt(resta)
##    print(f"Diferencia de distribuciones : {resultado}")
##    print(f"Estadístico de Chi-cuadrado: {chi2_stat}")
##    print(f"Valor p: {p_val}")
##    print("-------------------------------------------------------------")
##
##    print("\n GPT4turbo-GPT4o")
##    tabla_contingencia = pd.crosstab(df_resultadosGPT["gpt_4turbo"], df_resultadosGPT["gpt_4o"])
##    chi2_stat, p_val, dof, ex = chi2_contingency(tabla_contingencia)
##    resta =( df_resultadosGPT["gpt_4turbo"].std())** 2 - (df_resultadosGPT["gpt_4o"].std())** 2
##    resultado= np.sqrt(resta)
##    print(f"Diferencia de distribuciones : {resultado}")
##    print(f"Estadístico de Chi-cuadrado: {chi2_stat}")
##    print(f"Valor p: {p_val}")
##    print("-------------------------------------------------------------")
##
##    print("\n GPT4turbo-GPT4omini")
##    tabla_contingencia = pd.crosstab(df_resultadosGPT["gpt_4turbo"], df_resultadosGPT["gpt_4omini"])
##    chi2_stat, p_val, dof, ex = chi2_contingency(tabla_contingencia)
##    resta =( df_resultadosGPT["gpt_4turbo"].std())** 2 - (df_resultadosGPT["gpt_4omini"].std())** 2
##    resultado= np.sqrt(resta)
##    print(f"Diferencia de distribuciones : {resultado}")
##    print(f"Estadístico de Chi-cuadrado: {chi2_stat}")
##    print(f"Valor p: {p_val}")
##    print("-------------------------------------------------------------")
##
##    print("\n GPT4o-GPT4omini")
##    tabla_contingencia = pd.crosstab(df_resultadosGPT["gpt_4o"], df_resultadosGPT["gpt_4omini"])
##    chi2_stat, p_val, dof, ex = chi2_contingency(tabla_contingencia)
##    resta =( df_resultadosGPT["gpt_4o"].std())** 2 - (df_resultadosGPT["gpt_4omini"].std())** 2
##    resultado= np.sqrt(resta)
##    print(f"Diferencia de distribuciones : {resultado}")
##    print(f"Estadístico de Chi-cuadrado: {chi2_stat}")
##    print(f"Valor p: {p_val}")
##    print("-------------------------------------------------------------")

# Lee los excel con los resultados
dg_results_4o = pd.read_excel(
    os.path.join("..", "EXCEL FINAL MODELOS", "dictator_game_log_4o.xlsx")
)
dg_results_4omini = pd.read_excel(
    os.path.join("..", "EXCEL FINAL MODELOS", "dictator_game_log_4omini.xlsx")
)

dg_results_4 = pd.read_excel(
    os.path.join("..", "EXCEL FINAL MODELOS", "dictator_game_log_4.xlsx")
)
dg_results_4turbo = pd.read_excel(
    os.path.join("..", "EXCEL FINAL MODELOS", "dictator_game_log_4_turbo.xlsx")
)

dg_results_35_turbo = pd.read_excel(
    os.path.join("..", "EXCEL FINAL MODELOS", "dictator_game_log_35_turbo.xlsx")
)

# Función de llamada para producir tablas y figuras
produce_stadistics (dg_results_4,dg_results_4turbo, dg_results_4o, dg_results_4omini, dg_results_35_turbo)
