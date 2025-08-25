#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# app_prueba_Americo
import streamlit as st
import pandas as pd

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

# Convertir fecha a tipo datetime por si acaso
df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")

# 3. Interfaz Streamlit
st.title("Dashboard Oferta Loyalty")

# Filtros dinámicos
fecha_ini = st.date_input("Fecha inicio", value=df["Fecha"].min())
fecha_fin = st.date_input("Fecha fin", value=df["Fecha"].max())
monto_min = st.number_input("Monto mínimo", value=55000)

productos_oferta = st.multiselect(
    "Selecciona productos de la oferta", 
    options=df["ProductoID"].unique()
)

# 4. Calcular métricas
df_filtro = df[
    (df["Fecha"] >= pd.to_datetime(fecha_ini)) & 
    (df["Fecha"] <= pd.to_datetime(fecha_fin)) & 
    (df["ProductoID"].isin(productos_oferta))
]

num_clientes = df_filtro["ClienteID"].nunique()
num_transacciones = df_filtro["VentaID"].nunique()
venta_total = df_filtro["ValorVenta"].sum()

# 5. Mostrar resultados
st.metric("Clientes únicos", num_clientes)
st.metric("Número de transacciones", num_transacciones)
st.metric("Venta total oferta", venta_total)

# Pareto
pareto = df_filtro.groupby("ProductoID")["ValorVenta"].sum().reset_index()
pareto = pareto.sort_values(by="ValorVenta", ascending=False)
pareto["% acumulado"] = pareto["ValorVenta"].cumsum()/pareto["ValorVenta"].sum()

st.subheader("Pareto de productos")
st.dataframe(pareto)

