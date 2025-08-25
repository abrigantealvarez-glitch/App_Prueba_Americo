#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# app_prueba_Americo
import streamlit as st
import pandas as pd
from io import BytesIO

# 1. Cargar los datos
ventas = pd.read_csv("Ventas.csv")
productos = pd.read_csv("Productos.csv")
clientes = pd.read_csv("Clientes.csv")
negocios = pd.read_csv("Negocios.csv")
calendario = pd.read_csv("Calendario.csv")

# 2. Integrar los datos (merge)
df = ventas.merge(productos, on="ProductoID", how="left")
df = df.merge(clientes, on="ClienteID", how="left")
df = df.merge(negocios, on="NegocioID", how="left")
df = df.merge(calendario, on="Fecha", how="left")

# 3. Interfaz Streamlit
st.title("Dashboard Oferta Loyalty")

# Filtros dinámicos
fecha_ini = st.date_input("Fecha inicio")
fecha_fin = st.date_input("Fecha fin")
monto_min = st.number_input("Monto mínimo", value=55000)

productos_oferta = st.multiselect(
    "Selecciona productos de la oferta", 
    options=df["ProductoID"].unique()
)

# 4. Calcular métricas
df_filtro = df[
    (df["Fecha"] >= str(fecha_ini)) & 
    (df["Fecha"] <= str(fecha_fin)) & 
    (df["ProductoID"].isin(productos_oferta))
]

num_clientes = df_filtro["ClienteID"].nunique()
num_transacciones = df_filtro["VentaID"].nunique()
df_filtro["Monto"] = df_filtro["Cantidad"] * df_filtro["PrecioUnitario"]
venta_total = df_filtro["Monto"].sum()

# 5. Mostrar resultados
st.metric("Clientes únicos", num_clientes)
st.metric("Número de transacciones", num_transacciones)
st.metric("Venta total oferta", venta_total)

# Pareto
pareto = df_filtro.groupby("ProductoID")["Monto"].sum().reset_index()
pareto = pareto.sort_values(by="Monto", ascending=False)
pareto["% acumulado"] = pareto["Monto"].cumsum()/pareto["Monto"].sum()

st.subheader("Pareto de productos")
st.dataframe(pareto)

# 6. Exportar a Excel con openpyxl 
output = BytesIO()
df_filtro.to_csv(output, index=False, encoding="utf-8-sig")
st.download_button(
    
    label="📥 Descargar resultados en CSV",
    data=output.getvalue(),
    file_name="resultados_oferta_loyalty.csv",
    mime="text/csv"
)

