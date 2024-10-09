# Cargar las librerías necesarias
library(readxl)     # Para leer archivos Excel
library(nortest)    # Para realizar pruebas de normalidad (como la prueba de Lilliefors)
library(tidyverse)  # Para manipulación de datos y visualización (incluye dplyr, ggplot2, etc.)

# Establecer el directorio de trabajo donde se encuentran los archivos
setwd("C:/Users/valem/OneDrive - Estudiantes ITCR/TFG/APlicacion experimentos/EXCEL FINAL MODELOS")

# Verificar el directorio de trabajo actual
getwd()

# Leer el archivo Excel y almacenar los datos en un DataFrame llamado 'datos'
datos <- read_excel("DatosAnalisisANOVAv2-1.xlsx")

# Mostrar los primeros registros del DataFrame 'datos' para inspeccionar la estructura
head(datos)

# Contar el número de observaciones para cada modelo en la columna 'Modelo'
table(datos$Modelo)

# Verificar la estructura de la columna 'Allocation' para asegurarse de que sea del tipo correcto
str(datos$Allocation)

# Ajustar un modelo de análisis de varianza (ANOVA) para ver si hay diferencias significativas en 'Allocation' según el 'Modelo'
anova <- aov(datos$Allocation ~ datos$Modelo)

# Resumir los resultados del modelo ANOVA
summary(anova)

# Realizar la prueba de comparaciones múltiples de Tukey
# Esta prueba se utiliza para identificar diferencias significativas
# entre las medias de los grupos después de haber realizado el ANOVA.
# En este caso, estamos comparando las medias de 'Allocation' 
# entre diferentes modelos.

# Ejecutar Tukey HSD en el modelo ANOVA
TukeyHSD(anova)






