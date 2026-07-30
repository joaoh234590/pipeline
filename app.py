import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard Macroeconômico - BACEN",
    page_icon="📈",
    layout="wide"
)

# Título principal
st.title(" Análise de Ciclos e Tendências Macroeconômicas")
st.markdown("---")

# Menu lateral
st.sidebar.header("Painel de Controle")
indicador = st.sidebar.selectbox(
    "Selecione a Variável:",
    ["IBCR-NE (Atividade Econômica NE)", "IPCA (Inflação)", "Selic (Taxa Básica)"]
)

st.subheader(f"Indicador Selecionado: {indicador}")
st.info("Conecte aqui as funções de extração do Banco Central desenvolvidas no Colab.")
