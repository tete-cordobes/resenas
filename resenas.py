
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def calcular_fechas_de_reviews(url, fecha_revision, codigo_factura, nombre_negocio, nombre_proyecto, 
                              cantidad_reviews, reviews_por_mes, incremento_mensual):
    fecha_inicio = datetime.strptime(fecha_revision, "%d/%m/%Y")
    fechas = []
    review_actual = 1

    while review_actual <= cantidad_reviews:
        for _ in range(reviews_por_mes):
            if review_actual > cantidad_reviews:
                break
            fechas.append({
                "URL": url,
                "Fecha de Revisión": fecha_inicio.strftime("%d/%m/%Y"),
                "Código de Factura": codigo_factura,
                "Nombre del Negocio": nombre_negocio,
                "Nombre del Proyecto": nombre_proyecto,
                "Número de Review": review_actual
            })
            review_actual += 1
        fecha_inicio += timedelta(days=30)  # Incrementar un mes
        reviews_por_mes = int(reviews_por_mes * (1 + incremento_mensual / 100))  # Incrementar las reviews por mes

    return pd.DataFrame(fechas)

st.title('Planificador de Reviews')

# Sidebar para la entrada de datos
with st.sidebar:
    st.header("Datos de Entrada")
    url = st.text_input("URL:")
    fecha_revision = st.text_input("Fecha de Revisión (dd/mm/aaaa):")
    codigo_factura = st.text_input("Código de Factura:")
    nombre_negocio = st.text_input("Nombre del Negocio:")
    nombre_proyecto = st.text_input("Nombre del Proyecto:")
    cantidad_reviews = st.number_input("Cantidad de Reviews:", min_value=1, step=1)
    reviews_por_mes = st.number_input("Reviews por Mes:", min_value=1, step=1)
    incremento_mensual = st.number_input("Incremento Mensual (%):", step=1.0)

# Botón para ejecutar el cálculo
if st.sidebar.button("Calcular Fechas de Reviews"):
    if fecha_revision:
        df_reviews = calcular_fechas_de_reviews(url, fecha_revision, codigo_factura, nombre_negocio, 
                                                nombre_proyecto, cantidad_reviews, reviews_por_mes, incremento_mensual)
        st.write(df_reviews)
        st.download_button("Descargar CSV", df_reviews.to_csv(index=False), "reviews_por_mes.csv", "text/csv", key='download-csv')
