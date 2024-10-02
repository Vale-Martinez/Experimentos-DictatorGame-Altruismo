import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
import os
from statsmodels.graphics.factorplots import interaction_plot

# Configuración para mostrar todas las columnas
pd.set_option('display.max_columns', None)

# Carga de Datos
datos= pd.read_excel(
    os.path.join("..", "EXCEL FINAL MODELOS", "DatosAnalisisANOVA.xlsx")
)

# Muestra el resumen de la agrupación por 'Modelo' sin truncar columnas
print (datos.groupby('Modelo').describe())

# Diagrama Box-plot 1
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
axs[0].set_title('Fractcion vs Allocation')
sns.boxplot(x="Allocation", y="Fraction", data=datos, ax=axs[0])
sns.swarmplot(x="Allocation", y="Fraction", data=datos, color='black',
              alpha = 0.5, ax=axs[0])

axs[1].set_title('Fraction vs Modelo')
sns.boxplot(x="Modelo", y="Fraction", data=datos, ax=axs[1])
sns.swarmplot(x="Modelo", y="Fraction", data=datos, color='black',
              alpha = 0.5, ax=axs[1]);
fig.show()
# Diagrama Box-plot 2 
fig, ax = plt.subplots(1, 1, figsize=(8, 4))
ax.set_title('Fraction vs modelo y Allocation')
sns.scatterplot(x="Allocation", y="Fraction", hue='Modelo', data=datos, ax=ax, 
                palette="deep", s=100, alpha=0.7)

fig.show()

# Resultados medios y desviación típica por edad
print('Resultados medios y desviación típica por Asigancion')
print (datos.groupby('Allocation')['Fraction'].agg(['mean', 'std']))

# Resultados medios y desviación típica por sexo
print('Resultados medios y desviación típica por Modelo')
print(datos.groupby('Modelo')['Fraction'].agg(['mean', 'std']))

# Gráfico de interacciones
fig, ax = plt.subplots(figsize=(6, 4))
fig = interaction_plot(
    x        = datos.Allocation,
    trace    = datos.Modelo,
    response = datos.Fraction,
    ax       = ax,
    colors = ['green', 'orange','red','gray','blue','pink']
)
fig.show()

# Test ANOVA de dos vías (Two-way ANOVA)
print (pg.anova(
    data     = datos,
    dv       = 'Fraction',
    between  = ['Modelo', 'Allocation'],
    detailed = True
).round(4))
