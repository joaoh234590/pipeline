import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página web
st.set_page_config(page_title="Pipeline de Dados Econômicos", layout="wide")

st.title("Pipeline Universal e Reprodutível de Dados Econômicos")
st.markdown("Ferramenta de Ingestão Automatizada e Visualização Dinâmica de Séries Temporais.")

# ---------------------------------------------------------------------
# SIDEBAR: INGESTÃO DE DADOS
# ---------------------------------------------------------------------
st.sidebar.header("1. Seleção da Fonte")
tipo_fonte = st.sidebar.radio("Origem dos dados:", ["Código SGS/BACEN", "Link CSV / Arquivo Externo"])

if tipo_fonte == "Código SGS/BACEN":
    codigo_sgs = st.sidebar.text_input("Código da Série (ex: 25388 para IBCR-NE, 433 para IPCA):", value="25388")
    fonte = codigo_sgs
else:
    url_csv = st.sidebar.text_input("Cole a URL do arquivo CSV:")
    fonte = url_csv

sep = st.sidebar.text_input("Separador de colunas:", value=";")
decimal = st.sidebar.text_input("Separador decimal:", value=",")

# Função de Carregamento com Cache para Alta Performance
@st.cache_data
def carregar_dados(fonte, sep, decimal):
    if str(fonte).isdigit():
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{fonte}/dados?formato=csv"
        df = pd.read_csv(url, sep=sep, decimal=decimal)
    else:
        df = pd.read_csv(fonte, sep=sep, decimal=decimal)
    
    df.columns = [str(c).lower().strip() for c in df.columns]
    if 'data' in df.columns and 'valor' in df.columns:
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        df = df.dropna(subset=['data', 'valor'])
        df['ano'] = df['data'].dt.year
    return df

# ---------------------------------------------------------------------
# PROCESSAMENTO E RENDERIZAÇÃO
# ---------------------------------------------------------------------
if fonte:
    try:
        df = carregar_dados(fonte, sep, decimal)
        st.success(f"[SUCESSO] {len(df)} registros carregados!")

        # Exibir prévia da tabela de dados
        with st.expander("Ver Tabela de Dados Brutos"):
            st.dataframe(df, use_container_width=True)

        # SIDEBAR: CONFIGURAÇÃO DO GRÁFICO
        st.sidebar.header("2. Opções de Visualização")
        tipo_grafico = st.sidebar.selectbox(
            "Escolha o Tipo de Gráfico:",
            ["linha", "barra", "pizza", "histograma", "boxplot", "area", "dispersao"]
        )
        
        titulo_grafico = st.sidebar.text_input("Título do Gráfico:", value=f"Gráfico: {tipo_grafico.capitalize()}")
        cor_grafico = st.sidebar.color_picker("Cor do Gráfico:", value="#1f77b4")

        # RENDERIZAÇÃO DA FIGURA
        fig, ax = plt.subplots(figsize=(10, 5))
        df_plot = df.copy()

        if tipo_grafico == 'linha':
            ax.plot(df_plot['data'], df_plot['valor'], color=cor_grafico, linewidth=2)
            ax.set_xlabel('Anos')
            ax.set_ylabel('Valor')
            ax.grid(True, linestyle='--', alpha=0.4)

        elif tipo_grafico == 'barra':
            media_anual = df_plot.groupby('ano')['valor'].mean().reset_index()
            ax.bar(media_anual['ano'].astype(str), media_anual['valor'], color=cor_grafico, edgecolor='black', alpha=0.8)
            plt.xticks(rotation=45)
            ax.set_xlabel('Ano')
            ax.set_ylabel('Média Anual')
            ax.grid(axis='y', linestyle='--', alpha=0.4)

        elif tipo_grafico == 'pizza':
            df_plot['faixa_temp'] = pd.cut(df_plot['valor'], bins=3, labels=['Faixa Baixa', 'Faixa Média', 'Faixa Alta'])
            contagem = df_plot['faixa_temp'].value_counts()
            ax.pie(contagem, labels=contagem.index, autopct='%1.1f%%', startangle=140, colors=['#66b3ff', '#99ff99', '#ff9999'], wedgeprops={'edgecolor': 'black'})

        elif tipo_grafico == 'histograma':
            ax.hist(df_plot['valor'].dropna(), bins=20, color=cor_grafico, edgecolor='black', alpha=0.7)
            ax.set_xlabel('Valor')
            ax.set_ylabel('Frequência')
            ax.grid(True, linestyle='--', alpha=0.4)

        elif tipo_grafico == 'boxplot':
            sns.boxplot(y=df_plot['valor'], color=cor_grafico, ax=ax)

        elif tipo_grafico == 'area':
            ax.fill_between(df_plot['data'], df_plot['valor'], color=cor_grafico, alpha=0.4)
            ax.plot(df_plot['data'], df_plot['valor'], color=cor_grafico, linewidth=1.5)
            ax.set_xlabel('Anos')
            ax.set_ylabel('Valor')
            ax.grid(True, linestyle='--', alpha=0.4)

        elif tipo_grafico == 'dispersao':
            ax.scatter(df_plot['data'], df_plot['valor'], color=cor_grafico, alpha=0.7, edgecolors='black')
            ax.set_xlabel('Anos')
            ax.set_ylabel('Valor')
            ax.grid(True, linestyle='--', alpha=0.4)

        ax.set_title(titulo_grafico, fontsize=12, fontweight='bold', pad=15)
        plt.tight_layout()

        # Exibir o gráfico no Streamlit
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os dados ou gerar o gráfico: {e}")
