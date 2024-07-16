# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:23:44 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Datos de la tabla "Diversificación de la cartera por AFORE"
data = {
    'AFORE': ['Azteca', 'Citibanamex', 'Coppel', 'Inbursa', 'Invercap', 'PENSIONISSSTE',
              'Principal', 'Profuturo', 'SURA', 'XXI-Banorte'],
    'Renta Var. Nac.': [10.86, 4.64, 13.39, 11.26, 6.94, 7.43, 7.17, 8.12, 7.62, 6.78],
    'Renta Var. Intl.': [18.53, 10.70, 17.42, 7.65, 12.67, 11.26, 11.71, 11.53, 14.05, 13.50],
    'Mercancías': [np.nan, 0.18, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.18],
    'Deuda Priv. Nac.': [15.70, 13.92, 26.38, 21.59, 14.78, 14.21, 12.13, 9.25, 16.32, 13.11],
    'Estructurados': [4.64, 7.93, 7.81, 4.57, 5.04, 9.05, 11.40, 4.77, 9.13, 9.76],
    'FIBRAS': [4.29, 3.60, 4.64, 3.99, 2.58, 5.03, 2.64, 1.06, 2.99, 2.87],
    'Deuda Intl.': [0.04, 1.41, np.nan, 8.37, 1.20, 1.62, 3.44, 0.38, 1.02, 0.29],
    'Val. Gub.': [44.49, 57.50, 28.61, 41.67, 53.10, 51.20, 46.09, 61.95, 45.77, 51.36],
    'Otros/Divisas': [1.45, 0.13, 1.75, 0.90, 3.69, 0.19, 5.41, 2.94, 3.09, 2.15]
}

# Crear un DataFrame de Pandas
df = pd.DataFrame(data)

# Mostrar resultados
st.title('Diversificación de la cartera por AFORE')

# Tabla de datos
st.subheader('Datos de Diversificación por AFORE')
st.dataframe(df)

# Selección de AFOREs para incluir en la simulación
selected_afores = st.multiselect('Selecciona AFOREs para la asignación:', df['AFORE'])

# Input para el monto total de inversión
monto_total = st.number_input('Ingrese el monto total de inversión:', min_value=1000, step=1000)

# Botón para ejecutar la asignación de activos
ejecutar_asignacion = st.button('Ejecutar Asignación de Activos')

# Variable para almacenar la AFORE seleccionada
if selected_afores:
    selected_afore = selected_afores[0]  # Tomamos la primera AFORE seleccionada
else:
    selected_afore = None

if ejecutar_asignacion:
    if not selected_afores:
        st.warning('Por favor selecciona al menos una AFORE para la simulación')
    else:
        # Filtrar los datos para las AFOREs seleccionadas
        selected_data = df[df['AFORE'].isin(selected_afores)].reset_index(drop=True)

        # Calcular inversión proporcional para cada categoría
        inversion_proporcional = (selected_data.drop(columns=['AFORE']) * monto_total / 100).round(2)
        
        # Llenar valores NaN con 0
        inversion_proporcional = inversion_proporcional.fillna(0)
        
        # Agregar el monto total invertido
        inversion_proporcional['Monto total de Inversión'] = monto_total

        # Crear un DataFrame resultado con las inversiones proporcionales
        df_resultado = pd.concat([selected_data[['AFORE']], inversion_proporcional], axis=1)

        # Mostrar el DataFrame resultado
        st.subheader('Proporción de Activos por AFORE')
        st.dataframe(df_resultado)

        # Crear un gráfico de barras individuales
        fig = px.bar(
            df_resultado.melt(id_vars=['AFORE'], var_name='Categoría', value_name='Monto de Inversión'),
            x='AFORE',
            y='Monto de Inversión',
            color='Categoría',
            barmode='group',
            title='Asignación de Activos por AFORE'
        )

        # Ajustar el tamaño del gráfico
        fig.update_layout(
            width=1600,
            height=700
        )

        # Mostrar el gráfico de barras individuales
        st.plotly_chart(fig)

# Gráfico de torta dinámico según las AFOREs seleccionadas
if selected_afores:
    st.subheader(f'Distribución de Activos para AFOREs seleccionadas')

    # Filtrar los datos para las AFOREs seleccionadas
    data_selected_afores = df[df['AFORE'].isin(selected_afores)]

    # Crear el gráfico de torta
    fig_pie = px.pie(
        data_selected_afores.melt(id_vars=['AFORE'], var_name='Categoría', value_name='Monto de Inversión'),
        names='Categoría',
        values='Monto de Inversión',
        title=f'Distribución de Activos para AFOREs seleccionadas'
    )

    # Ajustar el tamaño del gráfico de torta
    fig_pie.update_layout(
        width=800,
        height=600
    )

    # Mostrar el gráfico de torta
    st.plotly_chart(fig_pie)

# Resumen estadístico de la asignación de activos para AFOREs seleccionadas
if ejecutar_asignacion and 'df_resultado' in locals():
    st.subheader('Resumen Estadístico por AFORE')
    for afore in selected_afores:
        st.subheader(f'Resumen Estadístico para {afore}')
        st.write(df_resultado[df_resultado['AFORE'] == afore].drop(columns=['AFORE']).sum())

# Sección de ayuda
st.sidebar.title("Ayuda")
st.sidebar.info("""
Esta aplicación permite visualizar y simular la diversificación de la cartera de inversión de diferentes AFOREs (Administradoras de Fondos para el Retiro). 
- **Datos de Diversificación por AFORE**: Muestra una tabla con la distribución de las inversiones en distintas categorías para cada AFORE.
- **Selección de AFOREs para la asignación**: Permite seleccionar una o más AFOREs para incluirlas en la simulación de asignación de activos.
- **Monto total de inversión**: Permite ingresar el monto total de la inversión para distribuirlo proporcionalmente entre las categorías de inversión de las AFOREs seleccionadas.
- **Ejecutar Asignación de Activos**: Realiza la simulación de asignación de activos para las AFOREs seleccionadas basado en el monto total de inversión ingresado.
- **Proporción de Activos por AFORE**: Muestra una tabla con la asignación proporcional del monto de inversión entre las categorías de cada AFORE seleccionada.
- **Gráfico de Barras**: Visualiza la asignación de activos en un gráfico de barras agrupadas por AFORE y categoría de inversión.
- **Gráfico de Torta Dinámico**: Muestra la distribución de activos en un gráfico de torta para las AFOREs seleccionadas.
- **Resumen Estadístico**: Proporciona un resumen del total invertido y la asignación por categoría para las AFOREs seleccionadas, después de ejecutar la asignación de activos.
""")

# Copyright
st.sidebar.text("© 2024 Todos los derechos reservados. Creado por jahoperi")
