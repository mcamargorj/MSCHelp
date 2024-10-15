import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import io
import chardet
from PIL import Image
import matplotlib.pyplot as plt

# Configurar layout da página
st.set_page_config(
    page_title="Visualizador de Dados",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

def mostrar_logo():
    logo = Image.open('logo1.png').convert("RGBA")
    logo = logo.resize((200, 200))  # Redimensiona a imagem para 200x200 pixels
    
    # Exibir a imagem diretamente na barra lateral
    st.sidebar.image(logo, use_column_width=True)  # Ajusta o tamanho da imagem à largura da sidebar


def principal():
    st.title("📊 Análise de Dados Impactante")

    mostrar_logo()  # Mostrar a logo na sidebar

    st.header("Faça o upload do seu arquivo de dados")
    arquivo_csv = st.file_uploader("Carregar arquivo CSV", type=["csv"], help="Envie seu arquivo CSV aqui")

    if arquivo_csv is not None:
        codificacao = chardet.detect(arquivo_csv.getvalue())['encoding']
        delimitadores = [',', ';', '\t', '|', ' ']
        conteudo_csv = None
        dados = None
        
        # Tentativa de leitura do arquivo CSV com diferentes delimitadores
        for delimitador in delimitadores:
            try:
                conteudo_csv = arquivo_csv.getvalue().decode(codificacao)
                dados = pd.read_csv(io.StringIO(conteudo_csv), sep=delimitador)
                if len(dados.columns) > 1:
                    break
            except Exception:
                continue

        # Caso a leitura falhe
        if dados is None or len(dados.columns) == 1:
            st.warning("Falha na detecção automática do delimitador. Por favor, selecione o delimitador correto.")
            delimitador_escolhido = st.selectbox("Escolha o delimitador", delimitadores)
            try:
                dados = pd.read_csv(io.StringIO(conteudo_csv), sep=delimitador_escolhido)
            except Exception as e:
                st.error(f"Erro ao ler o arquivo CSV: {e}")
                return

        # Exibir uma visão geral dos dados
        st.write("### Visão geral dos dados:")
        st.write(dados.head())

        st.sidebar.header("Visualizações")
        opcoes_graficos = ["Gráfico de barras", "Gráfico de dispersão", "Histograma", "Box plot"]
        grafico_selecionado = st.sidebar.selectbox("Escolha um tipo de gráfico", opcoes_graficos)

        sns.set(style="whitegrid")  # Estilo do gráfico

        if grafico_selecionado == "Gráfico de barras":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)
            eixo_y = st.sidebar.selectbox("Selecione o eixo y", dados.columns)
            st.write("### Gráfico de Barras:")
            figura, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=dados[eixo_x], y=dados[eixo_y], ax=ax, palette="viridis")
            ax.set_title(f'Gráfico de Barras: {eixo_y} por {eixo_x}', fontsize=16)
            ax.set_xlabel(eixo_x, fontsize=14)
            ax.set_ylabel(eixo_y, fontsize=14)
            st.pyplot(figura)

        elif grafico_selecionado == "Gráfico de dispersão":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)
            eixo_y = st.sidebar.selectbox("Selecione o eixo y", dados.columns)

            if pd.to_datetime(dados[eixo_x], errors='coerce').notnull().all():
                st.write("### Gráfico de Dispersão:")
                figura, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(x=pd.to_datetime(dados[eixo_x]), y=dados[eixo_y], ax=ax, color='blue', s=100, alpha=0.7)
                ax.set_title(f'Gráfico de Dispersão: {eixo_y} por {eixo_x}', fontsize=16)
                ax.set_xlabel(eixo_x, fontsize=14)
                ax.set_ylabel(eixo_y, fontsize=14)
                st.pyplot(figura)
            else:
                st.warning("A coluna selecionada para o eixo X não contém dados de data válidos.")

        elif grafico_selecionado == "Histograma":
            coluna = st.sidebar.selectbox("Selecione uma coluna", dados.columns)
            numero_bins = st.sidebar.slider("Número de intervalos (bins)", 5, 100, 20)
            st.write("### Histograma:")
            figura, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(dados[coluna], bins=numero_bins, ax=ax, color='orange', kde=True)
            ax.set_title(f'Histograma da coluna: {coluna}', fontsize=16)
            ax.set_xlabel(coluna, fontsize=14)
            ax.set_ylabel("Frequência", fontsize=14)
            st.pyplot(figura)

        elif grafico_selecionado == "Box plot":
            coluna = st.sidebar.selectbox("Selecione uma coluna", dados.columns)
            st.write("### Box Plot:")
            figura, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(y=dados[coluna], ax=ax, palette="Set2")
            ax.set_title(f'Box Plot da coluna: {coluna}', fontsize=16)
            ax.set_ylabel(coluna, fontsize=14)
            st.pyplot(figura)

if __name__ == "__main__":
    principal()
