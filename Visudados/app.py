import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import io
import chardet
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import requests

# Configurar layout da página
st.set_page_config(
    page_title="Visualizador de Dados - VisuCSV",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

def mostrar_logo():
    logo = Image.open('logo1.png').convert("RGBA")
    logo = logo.resize((500, 500))  # Redimensiona a imagem para 200x200 pixels
    st.sidebar.image(logo, use_column_width=True)

# Função para localizar colunas que contêm variações de "data" e aplicar formatação

def formatar_coluna_data(dados):
    colunas_com_data = [coluna for coluna in dados.columns if 'data' in coluna.lower()]
    
    if colunas_com_data:
        # Se houver mais de uma coluna de data, permita que o usuário escolha uma
        if len(colunas_com_data) > 1:
            st.sidebar.header("Seleção da Coluna Data")
            coluna = st.sidebar.selectbox("Selecione a Coluna Data a ser considerada para análise", colunas_com_data)
        else:
            # Se houver apenas uma coluna de data, use-a diretamente
            coluna = colunas_com_data[0]
            st.success(f"A coluna '{coluna}' foi automaticamente selecionada para análise.")
        
        try:
            if dados[coluna].astype(str).str.match(r'^\d{6}$').all():
                dados['Data_Ajustada'] = pd.to_datetime(dados[coluna].astype(str), format='%Y%m', errors='coerce')
                st.success(f"Coluna '{coluna}' detectada no formato 'yyyymm' e convertida para data.")
            else:
                dados['Data_Ajustada'] = pd.to_datetime(dados[coluna], errors='coerce')

            dados['Ano'] = dados['Data_Ajustada'].dt.strftime('%Y')
            dados['Semestre'] = np.where(dados['Data_Ajustada'].dt.month <= 6, 1, 2)
            dados['Trimestre'] = ((dados['Data_Ajustada'].dt.month - 1) // 3) + 1
            dados['Mês-Ano'] = dados['Data_Ajustada'].dt.strftime('%m/%Y')
            dados['Data_Ajustada'] = dados['Data_Ajustada'].dt.strftime('%d/%m/%Y')
            #dados = dados.drop(columns=[coluna])

        except Exception as e:
            st.warning(f"Não foi possível converter a coluna '{coluna}' para data: {e}")
    else:
        st.warning("Nenhuma coluna de data encontrada.")
    
    return dados


def principal():
    st.title("📊 Análise de Dados com VisuCSV")
    mostrar_logo()

    st.header("Carregue ou forneça a URL do arquivo de dados")

    # Inicializa o session state se não existir
    if 'url_csv' not in st.session_state:
        st.session_state.url_csv = ""

    # Opção de carregar um arquivo CSV
    arquivo_csv = st.file_uploader("Carregar arquivo CSV.", type=["csv"], help="Envie seu arquivo CSV aqui")

    # Opção de fornecer uma URL para o CSV
    url_csv = st.text_input("Ou insira a URL do arquivo CSV.", help="Informe a URL para fazer o download do CSV")
    dados = None

    # Botões para carregar bases fictícias
    st.write("### 📂 Bases Fictícias:")
    if st.button("Base 1"):
        st.session_state.url_csv = "https://drive.google.com/uc?id=1FLNVucw0ObcbE6PLoK4hxXV4pPQFqiN7"
        st.success(f"URL selecionada: {st.session_state.url_csv}")

    if st.button("Base 2"):
        st.session_state.url_csv = "https://drive.google.com/uc?id=1w_k9ZWPDGiZyZWCaZhTx7lMMTInwlsKP"
        st.success(f"URL selecionada: {st.session_state.url_csv}")

    # Se a URL não estiver vazia, usa a URL do session state
    if st.session_state.url_csv:
        url_csv = st.session_state.url_csv
        

##
    def detectar_delimitador(conteudo_csv):
        delimitadores = [';', ',', '\t', '|', ' ']
        
        for delimitador in delimitadores:
            try:
                dados = pd.read_csv(io.StringIO(conteudo_csv), sep=delimitador)
                if len(dados.columns) > 1:
                    return dados
            except Exception as e:
                st.warning(f"Erro ao tentar ler com o delimitador '{delimitador}': {e}")
                continue
        return None

    if arquivo_csv is not None:
        # Tentar detectar a codificação do arquivo CSV
        codificacao = chardet.detect(arquivo_csv.getvalue())['encoding']
        conteudo_csv = arquivo_csv.getvalue().decode(codificacao)
        dados = detectar_delimitador(conteudo_csv)

        if dados is None or len(dados.columns) == 1:
            st.warning("Falha na detecção automática do delimitador. Por favor, selecione o delimitador correto.")
            delimitador_escolhido = st.selectbox("Escolha o delimitador", [';', ',', '\t', '|', ' '])
            try:
                dados = pd.read_csv(io.StringIO(conteudo_csv), sep=delimitador_escolhido)
            except Exception as e:
                st.error(f"Erro ao ler o arquivo CSV: {e}")
                return

    elif url_csv:
        try:
            response = requests.get(url_csv)
            response.raise_for_status()  # Verificar se houve erro no download
            conteudo_csv = response.content  # Pegar o conteúdo bruto

            # Detectar codificação do conteúdo baixado
            codificacao = chardet.detect(conteudo_csv)['encoding']
            conteudo_csv = conteudo_csv.decode(codificacao)

            dados = detectar_delimitador(conteudo_csv)

            if dados is None or len(dados.columns) == 1:
                st.warning("Falha na detecção automática do delimitador. Por favor, selecione o delimitador correto.")
                delimitador_escolhido = st.selectbox("Escolha o delimitador", [';', ',', '\t', '|', ' '])
                try:
                    dados = pd.read_csv(io.StringIO(conteudo_csv), sep=delimitador_escolhido)
                except Exception as e:
                    st.error(f"Erro ao ler o arquivo CSV: {e}")
                    return

            st.success(f"Arquivo CSV baixado com sucesso da URL fornecida.")
        except Exception as e:
            st.error(f"Erro ao baixar ou processar o arquivo CSV da URL: {e}")
            return
    
    if dados is not None:
        dadosorigem = dados.copy()
        # Aplicar a formatação nas colunas de data
        dados1 = formatar_coluna_data(dados)

        # Exibir uma tabela interativa
        st.write("### Tabela de dados (com os 5 primeiros registros):")
        st.dataframe(dados1.head(), use_container_width=True, hide_index=True)

        

        # Estatísticas descritivas
        desc = dados1.describe()

        # Adicionando legendas personalizadas
        legendas = {
            
            'mean': 'Média',
            'std': 'Desvio Padrão',
            'min': 'Mínimo',
            '25%': '1º Quartil',
            '50%': 'Mediana (2º Quartil)',
            '75%': '3º Quartil',
            'max': 'Máximo'
        }
        # Remover a linha 'count' (Número de Linhas Válidas)
        desc = desc.drop('count')


        # Renomeando as linhas com as legendas
        desc.rename(index=legendas, inplace=True)

        # Definir o número de linhas e colunas
        num_linhas = dadosorigem.shape[0]
        num_colunas = dadosorigem.shape[1]

        # Criando um DataFrame com o número de linhas e colunas
        info_adicional = pd.DataFrame({
            'Número de Linhas': [num_linhas],
            'Número de Colunas': [num_colunas]
        })

        # Exibindo as informações no Streamlit
        st.write("### Estatísticas Descritivas:")
        st.write(f"**Número de Linhas:** {num_linhas}")
        st.write(f"**Número de Colunas:** {num_colunas}")

        # Exibindo as estatísticas descritivas
        st.write(desc)




        # Seção de visualizações
        st.sidebar.header("Visualizações")
        opcoes_graficos = [
            "Gráfico de Barras 1",
            "Gráfico de Barras 2", 
            "Gráfico de Barras 3", 
            "Gráfico de Barras 4",
            "Gráfico de Barras 5",
            "Gráfico de Pizza", 
            "Gráfico de Linhas 1",
            "Gráfico de Linhas 2",
            "Gráfico de Linhas 3", 
            
        ]
        grafico_selecionado = st.sidebar.selectbox("Escolha um tipo de gráfico", opcoes_graficos)

        sns.set(style="whitegrid")

        # Escolha da paleta de cores
        paletas = {
            "Viridis": "viridis",
            "Blues": "Blues",
            "Pastel": "pastel",
            "Colorblind": "colorblind",
            "Dark": "dark"
        }
        paleta_escolhida = st.sidebar.selectbox("Escolha a paleta de cores", list(paletas.keys()))
        sns.set_palette(paletas[paleta_escolhida])

        # Ajuste do tamanho do gráfico com um único slider
        tamanho_grafico = st.sidebar.slider("Tamanho do Gráfico (5 a 15)", min_value=5, max_value=15, value=10)
        largura = tamanho_grafico
        altura = tamanho_grafico * 0.6  # Ajustando a altura para ser proporcional à largura
          
        # Função para formatar o eixo y como moeda brasileira
        def formatar_moeda(valor, pos):
            return f'R${valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

        # Função para formatar quantidade sem casas decimais
        def formatar_quantidade(valor, pos):
            return f'{int(valor):,}'.replace(',', '.')
        
        
                # Gráfico de Barras 1
        if grafico_selecionado == "Gráfico de Barras 1":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)
            eixo_y = st.sidebar.selectbox("Selecione o eixo y", dados.columns)
             # Verifica se as colunas são diferentes
            if eixo_x == eixo_y:
                st.error("As colunas selecionadas para os eixos x e y devem ser diferentes.")
            else:
                tipo_aggregacao = st.sidebar.selectbox("Selecione o tipo de agregação", ["Total", "Média"])
                
                st.write("### Gráfico de Barras 1:")

                # Criando a figura e o eixo
                figura, ax = plt.subplots(figsize=(10, 6))

                # Verificar se o eixo y contém valores numéricos
                if dados[eixo_y].dtype not in [np.int64, np.float64]:
                    st.warning(f"A coluna '{eixo_y}' do eixo Y contém valores não numéricos. Os rótulos não serão exibidos.")
                else:
                    # Agregando os dados de acordo com a escolha do usuário
                    if tipo_aggregacao == "Média":
                        dados_agregados = dados.groupby(eixo_x)[eixo_y].mean().reset_index()
                    else:  # Total
                        dados_agregados = dados.groupby(eixo_x)[eixo_y].sum().reset_index()

                    # Criando o gráfico de barras horizontal
                    sns.barplot(y=dados_agregados[eixo_x], x=dados_agregados[eixo_y], ax=ax, palette=paletas[paleta_escolhida], alpha=0.8, ci=None, orient='h')
                    
                    # Adiciona legendas ao final das barras
                    for p in ax.patches:
                        valor_x = p.get_width()

                        # Verifica se o eixo y deve ser formatado como moeda ou quantidade
                        if "R$" in dados[eixo_y].name or "valor" in eixo_y.lower():
                            ax.annotate(formatar_moeda(valor_x, None),  # Formatação de moeda
                                        (valor_x, p.get_y() + p.get_height() / 2), 
                                        ha='left', va='center', fontsize=10, color='black', rotation=0)  # Rotação a 0º
                        else:
                            ax.annotate(formatar_quantidade(valor_x, None),  # Formatação de quantidade
                                        (valor_x, p.get_y() + p.get_height() / 2), 
                                        ha='left', va='center', fontsize=10, color='black', rotation=0)  # Rotação a 0º

                    # Ajustar limite do eixo x para evitar que valores transponham a grade de fundo
                    ax.set_xlim(0, ax.get_xlim()[1] * 1.5)  # Aumenta o limite superior em 50%

                    # Formata eixo x como moeda ou quantidade
                    if "R$" in dados[eixo_y].name or "valor" in eixo_y.lower():
                        ax.xaxis.set_major_formatter(FuncFormatter(formatar_moeda))
                    else:
                        ax.xaxis.set_major_formatter(FuncFormatter(formatar_quantidade))

                    # Ajustando título e rótulos
                    ax.set_title(f'Gráfico de Barras: {tipo_aggregacao} de {eixo_y} por {eixo_x}', fontsize=16)
                    ax.set_xlabel(eixo_y, fontsize=14)
                    ax.set_ylabel("")  # Oculta o rótulo do eixo Y

                    # Melhorando a visualização
                    ax.grid(True, linestyle='--', alpha=0.7)  # Adicionando uma grade com estilo

                    # Ajustar automaticamente o layout para evitar que elementos fiquem fora da área visível
                    plt.tight_layout()
                    # Ocultando todos os rótulos do eixo X
                    ax.set_xticklabels([])

                    # Exibindo o gráfico no Streamlit
                    st.pyplot(figura)

        
  

        #Gráfico de Barras 2
        if grafico_selecionado == "Gráfico de Barras 2":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)  # Coluna para o eixo x (ex: Mês)
            eixo_valor = st.sidebar.selectbox("Selecione o eixo y (Valores)", dados.columns)  # Coluna para os valores

            # Verifica se as colunas são diferentes
            if eixo_x == eixo_valor:
                st.error("As colunas selecionadas para os eixos x e y devem ser diferentes.")
            else:
                # Adiciona opção de agregação
                tipo_aggregacao = st.sidebar.selectbox("Selecione o tipo de agregação", ["Total", "Média"])
                
                st.write("### Gráfico de Barras 2:")
                figura, ax = plt.subplots(figsize=(largura, altura))

                # Verificar se a coluna selecionada para o eixo Y contém valores numéricos
                if not pd.api.types.is_numeric_dtype(dados[eixo_valor]):
                    st.warning(f"A coluna '{eixo_valor}' não contém valores numéricos. O gráfico não pode ser gerado.")
                else:
                    # Agregar dados com base na opção escolhida
                    if tipo_aggregacao == "Total":
                        dados_agrupados = dados.groupby(eixo_x)[eixo_valor].sum().reset_index()
                    else:  # Média
                        dados_agrupados = dados.groupby(eixo_x)[eixo_valor].mean().reset_index()

                    # Criando o gráfico de barras com os totais
                    sns.barplot(x=eixo_x, y=eixo_valor, data=dados_agrupados, ax=ax, 
                                palette=paletas[paleta_escolhida], alpha=0.8)

                    # Adiciona legendas acima das barras (apenas para o valor total)
                    for p in ax.patches:
                        valor_y = p.get_height()
                        
                        if valor_y > 0:  # Verifica se o valor é maior que 0
                            if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower():
                                ax.annotate(formatar_moeda(valor_y, None),
                                            (p.get_x() + p.get_width() / 2., valor_y + 0.1 * valor_y),
                                            ha='center', va='bottom', fontsize=10, color='black', rotation=90)
                            else:
                                ax.annotate(formatar_quantidade(valor_y, None),
                                            (p.get_x() + p.get_width() / 2., valor_y + 0.1 * valor_y),
                                            ha='center', va='bottom', fontsize=10, color='black', rotation=90)

                    # Ajustar limite do eixo y
                    ax.set_ylim(0, ax.get_ylim()[1] * 1.5)

                    # Formata eixo y como moeda ou quantidade
                    if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower():
                        ax.yaxis.set_major_formatter(FuncFormatter(formatar_moeda))
                    else:
                        ax.yaxis.set_major_formatter(FuncFormatter(formatar_quantidade))

                    # Ajustando título e rótulos
                    ax.set_title(f'Gráfico de Barras: {tipo_aggregacao} de {eixo_valor} por {eixo_x}', fontsize=16)
                    ax.set_xlabel(eixo_x, fontsize=14)
                    ax.set_ylabel(eixo_valor, fontsize=14)

                    # Melhorando a visualização
                    plt.xticks(rotation=45)  # Girando rótulos do eixo x para 45 graus
                    ax.grid(True, linestyle='--', alpha=0.7)  # Adicionando uma grade com estilo

                    st.pyplot(figura)

    

        
        # Gráfico de Barras 3
        if grafico_selecionado == "Gráfico de Barras 3":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)  # Coluna para o eixo x (ex: Mês)
            eixo_valor = st.sidebar.selectbox("Selecione o eixo y (Valores)", dados.columns)  # Coluna para os valores
            eixo_produto = st.sidebar.selectbox("Selecione o eixo z (Produtos)", dados.columns)  # Coluna para produtos

            # Verifica se as colunas são diferentes
            if eixo_x == eixo_valor or eixo_x == eixo_produto or eixo_valor == eixo_produto:
                st.error("As colunas selecionadas para os eixos x, y e z devem ser diferentes.")
            else:
                # Verificar se a coluna selecionada para o eixo Y contém valores numéricos
                if not pd.api.types.is_numeric_dtype(dados[eixo_valor]):
                    st.warning(f"A coluna '{eixo_valor}' do eixo Y não contém valores numéricos. O gráfico não pode ser gerado.")
                else:
                    # Adiciona opção de agregação
                    tipo_aggregacao = st.sidebar.selectbox("Selecione o tipo de agregação", ["Total", "Média"])
                    
                    st.write("### Gráfico de Barras 3:")
                    figura, ax = plt.subplots(figsize=(largura, altura))

                    # Agregar dados com base na opção escolhida
                    if tipo_aggregacao == "Total":
                        dados_agrupados = dados.groupby([eixo_x, eixo_produto])[eixo_valor].sum().reset_index()
                    else:  # Média
                        dados_agrupados = dados.groupby([eixo_x, eixo_produto])[eixo_valor].mean().reset_index()

                    # Criando o gráfico de barras com hue para os produtos
                    sns.barplot(x=eixo_x, y=eixo_valor, hue=eixo_produto, data=dados_agrupados, ax=ax, 
                                palette=paletas[paleta_escolhida], alpha=0.8, errorbar=None)

                    # Adiciona legendas acima das barras
                    for p in ax.patches:
                        valor_y = p.get_height()

                        if valor_y > 0:  # Verifica se o valor é maior que 0
                            # Verifica se o eixo y deve ser formatado como moeda ou quantidade
                            if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower():
                                ax.annotate(formatar_moeda(valor_y, None),
                                            (p.get_x() + p.get_width() / 2., valor_y), 
                                            ha='center', va='bottom', fontsize=10, color='black', rotation=75)
                            else:
                                ax.annotate(formatar_quantidade(valor_y, None),
                                            (p.get_x() + p.get_width() / 2., valor_y), 
                                            ha='center', va='bottom', fontsize=10, color='black', rotation=75)

                    # Ajustar limite do eixo y
                    ax.set_ylim(0, ax.get_ylim()[1] * 1.3)

                    # Formata eixo y como moeda ou quantidade
                    if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower():
                        ax.yaxis.set_major_formatter(FuncFormatter(formatar_moeda))
                    else:
                        ax.yaxis.set_major_formatter(FuncFormatter(formatar_quantidade))

                    # Ajustando título e rótulos
                    ax.set_title(f'Gráfico de Barras: {tipo_aggregacao} de {eixo_valor} por {eixo_x}', fontsize=16)
                    ax.set_xlabel(eixo_x, fontsize=14)
                    ax.set_ylabel(eixo_valor, fontsize=14)

                    # Melhorando a visualização
                    plt.xticks(rotation=45)  # Girando rótulos do eixo x para 45 graus
                    ax.grid(True, linestyle='--', alpha=0.7)  # Adicionando uma grade com estilo

                    st.pyplot(figura)


    
        # Gráfico de Barras 4
        if grafico_selecionado == "Gráfico de Barras 4":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)  # Coluna para o eixo x (ex: Mês)
            eixo_valor = st.sidebar.selectbox("Selecione o eixo y (Valores)", dados.columns)  # Coluna para os valores

            # Verificar se o eixo x e o eixo y são a mesma coluna
            if eixo_x == eixo_valor:
                st.warning("As colunas selecionadas para os eixos x e y devem ser diferentes.")
            else:
                st.write("### Gráfico de Barras 4:")

                # Verificar se a coluna selecionada para o eixo Y contém valores numéricos
                if not pd.api.types.is_numeric_dtype(dados[eixo_valor]):
                    st.warning(f"A coluna '{eixo_valor}' não contém valores numéricos. O gráfico não pode ser gerado.")
                else:
                    figura, ax = plt.subplots(figsize=(largura, altura))

                    # Calcular o total de vendas por categoria
                    totais_por_categoria = dados.groupby(eixo_x)[eixo_valor].sum().reset_index()

                    # Criando o gráfico de barras com os totais
                    sns.barplot(x=eixo_x, y=eixo_valor, data=totais_por_categoria, ax=ax, palette=paletas[paleta_escolhida], alpha=0.8)

                    # Adiciona legendas acima das barras (apenas para o valor total)
                    for p in ax.patches:
                        valor_y = p.get_height()

                        if valor_y > 0:  # Verifica se o valor é maior que 0
                            if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower():
                                ax.annotate(formatar_moeda(valor_y, None),
                                            (p.get_x() + p.get_width() / 2., valor_y + 0.1 * valor_y),
                                            ha='left', va='bottom', fontsize=10, color='black', rotation=90)
                            else:
                                ax.annotate(formatar_quantidade(valor_y, None),
                                            (p.get_x() + p.get_width() / 2., valor_y + 0.1 * valor_y),
                                            ha='left', va='bottom', fontsize=10, color='black', rotation=90)

                    # Calcular a média de vendas por categoria
                    medias_por_categoria = dados.groupby(eixo_x)[eixo_valor].mean().reset_index()

                    # Ajustar limite do eixo y para evitar que valores transponham a grade de fundo
                    ax.set_ylim(0, ax.get_ylim()[1] * 2)

                    # Formata eixo y como moeda ou quantidade
                    if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower():
                        ax.yaxis.set_major_formatter(FuncFormatter(formatar_moeda))
                    else:
                        ax.yaxis.set_major_formatter(FuncFormatter(formatar_quantidade))

                    # Traçar a linha média e adicionar os valores médios próximos aos marcadores
                    media_y_values = medias_por_categoria[eixo_valor].tolist()
                    ax.plot(medias_por_categoria[eixo_x], media_y_values, color='blue', marker='o', linestyle='-', linewidth=2, label='Média', alpha=0.7)

                    for i, media_y in enumerate(media_y_values):
                        media_text = formatar_moeda(media_y, None) if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower() else formatar_quantidade(media_y, None)
                        ax.text(medias_por_categoria[eixo_x].iloc[i], media_y + 0.3 * media_y, media_text, color='blue', ha='right', fontsize=8, rotation=90, verticalalignment='bottom')

                    # Calcular e exibir o total geral
                    total_geral = totais_por_categoria[eixo_valor].sum()
                    total_text = formatar_moeda(total_geral, None) if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower() else formatar_quantidade(total_geral, None)

                    # Calcular a média total
                    media_total = medias_por_categoria[eixo_valor].mean()
                    media_total_text = formatar_moeda(media_total, None) if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower() else formatar_quantidade(media_total, None)

                    # Adicionar o total e a média na legenda, alinhado à direita
                    ax.legend(loc='upper right', title=f'Total: {total_text}\nMédia: {media_total_text}', fontsize=10)

                    # Ajustando título e rótulos
                    ax.set_title(f'Gráfico de Barras: {eixo_valor} por {eixo_x}', fontsize=16)
                    ax.set_xlabel(eixo_x, fontsize=14)
                    ax.set_ylabel(eixo_valor, fontsize=14)

                    # Melhorando a visualização
                    plt.xticks(rotation=45)  # Girando rótulos do eixo x para 45 graus
                    ax.grid(True, linestyle='--', alpha=0.7)  # Adicionando uma grade com estilo

                    # Exibindo o gráfico no Streamlit
                    st.pyplot(figura)

        # Gráfico de Barras 5
               
        if grafico_selecionado == "Gráfico de Barras 5":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)  # Coluna para o eixo x (ex: Mês)
            eixo_valor = st.sidebar.selectbox("Selecione o eixo y (Valores)", dados.columns)  # Coluna para os valores
            eixo_produto = st.sidebar.selectbox("Selecione o eixo z (Produtos)", dados.columns)  # Coluna para produtos

            # Verificar se os eixos são diferentes
            if eixo_x == eixo_valor or eixo_x == eixo_produto or eixo_valor == eixo_produto:
                st.warning("As colunas selecionadas para os eixos x, y e z devem ser diferentes.")
            else:
                st.write("### Gráfico de Barras 5:")

                # Verificar se a coluna selecionada para o eixo Y contém valores numéricos
                if not pd.api.types.is_numeric_dtype(dados[eixo_valor]):
                    st.warning(f"A coluna '{eixo_valor}' não contém valores numéricos. O gráfico não pode ser gerado.")
                else:
                    figura, ax = plt.subplots(figsize=(largura, altura))

                    # Calcular o total de valores agrupados por eixo_x e eixo_produto
                    totais_por_categoria = dados.groupby([eixo_x, eixo_produto])[eixo_valor].sum().reset_index()

                    # Criando o gráfico de barras com os totais
                    sns.barplot(x=eixo_x, y=eixo_valor, hue=eixo_produto, data=totais_por_categoria, ax=ax,
                                palette=paletas[paleta_escolhida], alpha=0.8)

                    # Adiciona legendas acima das barras (apenas para o valor total)
                    for p in ax.patches:
                        valor_y = p.get_height()

                        if valor_y > 0:  # Verifica se o valor é maior que 0
                            if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower():
                                ax.annotate(formatar_moeda(valor_y, None),
                                            (p.get_x() + p.get_width() / 2., valor_y + 0.1 * valor_y),
                                            ha='left', va='bottom', fontsize=10, color='black', rotation=90)
                            else:
                                ax.annotate(formatar_quantidade(valor_y, None),
                                            (p.get_x() + p.get_width() / 2., valor_y + 0.1 * valor_y),
                                            ha='left', va='bottom', fontsize=10, color='black', rotation=90)

                    # Calcular a média de valores por categoria (eixo_x e eixo_produto)
                    medias_por_categoria = dados.groupby([eixo_x, eixo_produto])[eixo_valor].mean().reset_index()

                    # Ajustar limite do eixo y para evitar que valores transponham a grade de fundo
                    ax.set_ylim(0, ax.get_ylim()[1] * 4)

                    # Formata eixo y como moeda ou quantidade
                    if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower():
                        ax.yaxis.set_major_formatter(FuncFormatter(formatar_moeda))
                    else:
                        ax.yaxis.set_major_formatter(FuncFormatter(formatar_quantidade))

                    # Traçar a linha média e adicionar os valores médios próximos aos marcadores
                    for produto in medias_por_categoria[eixo_produto].unique():
                        media_y_values = medias_por_categoria[medias_por_categoria[eixo_produto] == produto][eixo_valor].tolist()
                        x_values = medias_por_categoria[medias_por_categoria[eixo_produto] == produto][eixo_x].tolist()

                        ax.plot(x_values, media_y_values, marker='o', linestyle='-', linewidth=2, label=f'Média: {produto}', alpha=0.7)

                        for i, media_y in enumerate(media_y_values):
                            media_text = formatar_moeda(media_y, None) if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower() else formatar_quantidade(media_y, None)
                            ax.text(x_values[i], media_y + 0.03 * media_y, media_text, color='blue', ha='right', fontsize=8, rotation=90)

                    # Calcular e exibir o total geral
                    total_geral = totais_por_categoria[eixo_valor].sum()
                    total_text = formatar_moeda(total_geral, None) if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower() else formatar_quantidade(total_geral, None)

                    # Calcular a média total
                    media_total = medias_por_categoria[eixo_valor].mean()
                    media_total_text = formatar_moeda(media_total, None) if "R$" in dados[eixo_valor].name or "valor" in eixo_valor.lower() else formatar_quantidade(media_total, None)

                    # Adicionar o total e a média na legenda, alinhado à direita
                    ax.legend(loc='upper right', title=f'Total: {total_text}\nMédia: {media_total_text}', fontsize=10)
                    
                    

                    # Ajustando título e rótulos
                    ax.set_title(f'Gráfico de Barras: {eixo_valor} por {eixo_x} (dividido por {eixo_produto})', fontsize=16)
                    ax.set_xlabel(eixo_x, fontsize=14)
                    ax.set_ylabel(eixo_valor, fontsize=14)

                    # Melhorando a visualização
                    plt.xticks(rotation=45)  # Girando rótulos do eixo x para 45 graus
                    ax.grid(True, linestyle='--', alpha=0.7)  # Adicionando uma grade com estilo

                    # Exibindo o gráfico no Streamlit
                    st.pyplot(figura)



        # Gráfico de Dispersão
        elif grafico_selecionado == "Gráfico de Dispersão":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)
            eixo_y = st.sidebar.selectbox("Selecione o eixo y", dados.columns)
            st.write("### Gráfico de Dispersão:")
            
            figura, ax = plt.subplots(figsize=(largura, altura))

            # Adicionando o gráfico de dispersão
            sns.scatterplot(x=dados[eixo_x], y=dados[eixo_y], ax=ax,
                            hue=dados[eixo_y].astype(str),  # Converte o eixo Y para string para colorir
                            size=dados[eixo_y],  # Ajusta o tamanho dos pontos baseado no eixo Y
                            sizes=(20, 200),  # Define os tamanhos mínimo e máximo dos pontos
                            palette=paletas[paleta_escolhida],  # Usa a paleta de cores selecionada
                            alpha=0.7,  # Define a transparência dos pontos
                            edgecolor='w',  # Define a cor da borda dos pontos
                            linewidth=0.5)  # Define a largura da borda dos pontos

            # Ajustando títulos e rótulos
            ax.set_title(f'Gráfico de Dispersão: {eixo_x} vs {eixo_y}', fontsize=16)
            ax.set_xlabel(eixo_x, fontsize=14)
            ax.set_ylabel(eixo_y, fontsize=14)

            # Melhorando a visualização
            ax.grid(True, linestyle='--', alpha=0.7)  # Adicionando uma grade com estilo
            plt.xticks(rotation=45)  # Girando os rótulos do eixo x para melhor legibilidade

            st.pyplot(figura)


      # Histograma
        elif grafico_selecionado == "Histograma":
            # Filtrando as colunas numéricas
            colunas_numericas = dados.select_dtypes(include='number').columns
            
            coluna = st.sidebar.selectbox("Selecione a coluna numérica", colunas_numericas)
            
            # Permitir que o usuário escolha o número de bins
            num_bins = st.sidebar.slider("Número de Bins", min_value=5, max_value=100, value=30)
            
            st.write("### Histograma:")
            figura, ax = plt.subplots(figsize=(largura, altura))
            
            # Adicionando o histograma com KDE
            sns.histplot(dados[coluna], bins=num_bins, kde=True, ax=ax, palette=paletas[paleta_escolhida],
                        edgecolor='black', alpha=0.6)  # Adiciona contorno preto às barras

            # Estilizando título e rótulos
            ax.set_title(f'Histograma de {coluna}', fontsize=18, fontweight='bold')
            ax.set_xlabel(coluna, fontsize=14, fontweight='bold')
            ax.set_ylabel('Frequência', fontsize=14, fontweight='bold')

            # Adicionando a média e a mediana
            media = dados[coluna].mean()
            mediana = dados[coluna].median()
            ax.axvline(media, color='red', linestyle='dashed', linewidth=1.5, label='Média')
            ax.axvline(mediana, color='blue', linestyle='dashed', linewidth=1.5, label='Mediana')
            
            ax.legend()  # Adiciona a legenda

            # Melhorando a visualização
            ax.grid(True, linestyle='--', alpha=0.5)  # Adiciona uma grade com estilo
            plt.xticks(rotation=45)  # Girar os rótulos do eixo X para melhor legibilidade

            st.pyplot(figura)



        # Box Plot
        elif grafico_selecionado == "Box Plot":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)
            eixo_y = st.sidebar.selectbox("Selecione o eixo y", dados.columns)
            st.write("### Box Plot:")

            figura, ax = plt.subplots(figsize=(largura, altura))

            # Box plot com paleta de cores personalizada
            sns.boxplot(x=dados[eixo_x], y=dados[eixo_y], ax=ax, palette=paletas[paleta_escolhida])

            # Configurações visuais adicionais
            ax.set_title(f'Box Plot de {eixo_y} por {eixo_x}', fontsize=16, weight='bold')
            ax.set_xlabel(eixo_x, fontsize=14)
            ax.set_ylabel(eixo_y, fontsize=14)

            # Adicionando grid para facilitar a leitura
            ax.grid(True, linestyle='--', alpha=0.6)

            # Girar rótulos no eixo x se necessário para melhor visualização
            plt.xticks(rotation=45)

            st.pyplot(figura)
 
        # Gráfico de Linhas 1
       # Verifica se o gráfico selecionado é "Gráfico de Linhas 2"
        elif grafico_selecionado == "Gráfico de Linhas 1":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)
            eixo_y = st.sidebar.selectbox("Selecione o eixo y", dados.columns)
            tipo_aggregacao = st.sidebar.selectbox("Selecione o tipo de agregação", ["Total", "Média"])
            
            st.write("### Gráfico de Linhas 1:")

            # Criando a figura e o eixo
            figura, ax = plt.subplots(figsize=(largura, altura))

            # Verificar se o eixo y contém valores numéricos
            if dados[eixo_y].dtype not in [np.int64, np.float64]:
                st.warning(f"A coluna '{eixo_y}' do eixo Y contém valores não numéricos. Os rótulos não serão exibidos.")
            else:
                # Agregando os dados de acordo com a escolha do usuário
                if tipo_aggregacao == "Média":
                    dados_agregados = dados.groupby(eixo_x)[eixo_y].mean().reset_index()
                    valor_resumo = dados_agregados[eixo_y].mean()  # Calcula a média total
                    valor_label = f"Média: {formatar_moeda(valor_resumo, None)}"
                else:  # Total
                    dados_agregados = dados.groupby(eixo_x)[eixo_y].sum().reset_index()
                    valor_resumo = dados_agregados[eixo_y].sum()  # Calcula o total
                    valor_label = f"Total: {formatar_moeda(valor_resumo, None)}"

                # Criando o gráfico de linhas
                sns.lineplot(x=dados_agregados[eixo_x], y=dados_agregados[eixo_y], ax=ax, palette=paletas[paleta_escolhida], marker='o', label=valor_label)

                # Ajustar limite do eixo y para evitar que valores transponham a grade de fundo
                ax.set_ylim(0, ax.get_ylim()[1] * 1.1)  # Aumenta o limite superior em 10%

                # Formata eixo y como moeda ou quantidade
                if "R$" in dados[eixo_y].name or "valor" in eixo_y.lower():
                    ax.yaxis.set_major_formatter(FuncFormatter(formatar_moeda))
                else:
                    ax.yaxis.set_major_formatter(FuncFormatter(formatar_quantidade))

                # Ajustando título e rótulos
                ax.set_title(f'Gráfico de Linhas: {tipo_aggregacao} de {eixo_y} por {eixo_x}', fontsize=16)
                ax.set_xlabel(eixo_x, fontsize=14)
                ax.set_ylabel(eixo_y, fontsize=14)

                # Melhorando a visualização
                plt.xticks(rotation=45)  # Girando rótulos do eixo x para melhor leitura
                ax.grid(True, linestyle='--', alpha=0.7)  # Adicionando uma grade com estilo

                # Adiciona a legenda
                ax.legend()

                # Ajustar automaticamente o layout para evitar que elementos fiquem fora da área visível
                plt.tight_layout()

                # Ocultando rótulos "0" ou "R$0,00"
                labels = [item.get_text() for item in ax.get_xticklabels()]
                labels = ['' if label in ['0', 'R$0,00'] else label for label in labels]
                ax.set_xticklabels(labels)

                # Exibindo o gráfico no Streamlit
                st.pyplot(figura)


       # Verifica se o gráfico selecionado é "Gráfico de Linhas"
        elif grafico_selecionado == "Gráfico de Linhas 2":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)
            eixo_y = st.sidebar.selectbox("Selecione o eixo y", dados.columns)
            tipo_aggregacao = st.sidebar.selectbox("Selecione o tipo de agregação", ["Total", "Média"])
            
            st.write("### Gráfico de Linhas 2:")

            # Criando a figura e o eixo
            figura, ax = plt.subplots(figsize=(largura, altura))

            # Verificar se o eixo y contém valores numéricos
            if dados[eixo_y].dtype not in [np.int64, np.float64]:
                st.warning(f"A coluna '{eixo_y}' do eixo Y contém valores não numéricos. Os rótulos não serão exibidos.")
            else:
                # Agregando os dados de acordo com a escolha do usuário
                if tipo_aggregacao == "Média":
                    dados_agregados = dados.groupby(eixo_x)[eixo_y].mean().reset_index()
                else:  # Total
                    dados_agregados = dados.groupby(eixo_x)[eixo_y].sum().reset_index()

                # Criando o gráfico de linhas
                sns.lineplot(x=dados_agregados[eixo_x], y=dados_agregados[eixo_y], ax=ax, palette=paletas[paleta_escolhida], marker='o')

                # Adiciona legendas nos pontos da linha
                for x, y in zip(dados_agregados[eixo_x], dados_agregados[eixo_y]):
                    # Verifica se o eixo y deve ser formatado como moeda ou quantidade
                    if "R$" in dados[eixo_y].name or "valor" in eixo_y.lower():
                        ax.annotate(formatar_moeda(y, None),  # Formatação de moeda
                                    (x, y), 
                                    ha='center', va='bottom', fontsize=10, color='black')  # Rótulos acima dos pontos
                    else:
                        ax.annotate(formatar_quantidade(y, None),  # Formatação de quantidade
                                    (x, y), 
                                    ha='center', va='bottom', fontsize=10, color='black')  # Rótulos acima dos pontos

                # Ajustar limite do eixo y para evitar que valores transponham a grade de fundo
                ax.set_ylim(0, ax.get_ylim()[1] * 1.1)  # Aumenta o limite superior em 10%

                # Formata eixo y como moeda ou quantidade
                if "R$" in dados[eixo_y].name or "valor" in eixo_y.lower():
                    ax.yaxis.set_major_formatter(FuncFormatter(formatar_moeda))
                else:
                    ax.yaxis.set_major_formatter(FuncFormatter(formatar_quantidade))

                # Ajustando título e rótulos
                ax.set_title(f'Gráfico de Linhas: {tipo_aggregacao} de {eixo_y} por {eixo_x}', fontsize=16)
                ax.set_xlabel(eixo_x, fontsize=14)
                ax.set_ylabel(eixo_y, fontsize=14)

                # Melhorando a visualização
                plt.xticks(rotation=45)  # Girando rótulos do eixo x para melhor leitura
                ax.grid(True, linestyle='--', alpha=0.7)  # Adicionando uma grade com estilo

                # Ajustar automaticamente o layout para evitar que elementos fiquem fora da área visível
                plt.tight_layout()

                # Ocultando rótulos "0" ou "R$0,00"
                labels = [item.get_text() for item in ax.get_xticklabels()]
                labels = ['' if label in ['0', 'R$0,00'] else label for label in labels]
                ax.set_xticklabels(labels)

                # Exibindo o gráfico no Streamlit
                st.pyplot(figura)

        # Verifica se o gráfico selecionado é "Gráfico de Linhas"
        elif grafico_selecionado == "Gráfico de Linhas 3":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)
            eixo_y = st.sidebar.selectbox("Selecione o eixo y", dados.columns)
            tipo_aggregacao = st.sidebar.selectbox("Selecione o tipo de agregação", ["Total", "Média"])
            
            st.write("### Gráfico de Linhas 3:")

            # Criando a figura e o eixo
            figura, ax = plt.subplots(figsize=(largura, altura))

            # Verificar se o eixo y contém valores numéricos
            if dados[eixo_y].dtype not in [np.int64, np.float64]:
                st.warning(f"A coluna '{eixo_y}' do eixo Y contém valores não numéricos. Os rótulos não serão exibidos.")
            else:
                # Agregando os dados de acordo com a escolha do usuário
                if tipo_aggregacao == "Média":
                    dados_agregados = dados.groupby(eixo_x)[eixo_y].mean().reset_index()
                    valor_resumo = dados_agregados[eixo_y].mean()  # Calcula a média total
                    valor_label = f"Média: {formatar_moeda(valor_resumo, None)}"
                else:  # Total
                    dados_agregados = dados.groupby(eixo_x)[eixo_y].sum().reset_index()
                    valor_resumo = dados_agregados[eixo_y].sum()  # Calcula o total
                    valor_label = f"Total: {formatar_moeda(valor_resumo, None)}"

                # Criando o gráfico de linhas
                sns.lineplot(x=dados_agregados[eixo_x], y=dados_agregados[eixo_y], ax=ax, palette=paletas[paleta_escolhida], marker='o', label=valor_label)

                # Adiciona legendas nos pontos da linha
                for x, y in zip(dados_agregados[eixo_x], dados_agregados[eixo_y]):
                    # Verifica se o eixo y deve ser formatado como moeda ou quantidade
                    if "R$" in dados[eixo_y].name or "valor" in eixo_y.lower():
                        ax.annotate(formatar_moeda(y, None),  # Formatação de moeda
                                    (x, y), 
                                    ha='center', va='bottom', fontsize=10, color='black')  # Rótulos acima dos pontos
                    else:
                        ax.annotate(formatar_quantidade(y, None),  # Formatação de quantidade
                                    (x, y), 
                                    ha='center', va='bottom', fontsize=10, color='black')  # Rótulos acima dos pontos

                # Ajustar limite do eixo y para evitar que valores transponham a grade de fundo
                ax.set_ylim(0, ax.get_ylim()[1] * 1.1)  # Aumenta o limite superior em 10%

                # Formata eixo y como moeda ou quantidade
                if "R$" in dados[eixo_y].name or "valor" in eixo_y.lower():
                    ax.yaxis.set_major_formatter(FuncFormatter(formatar_moeda))
                else:
                    ax.yaxis.set_major_formatter(FuncFormatter(formatar_quantidade))

                # Ajustando título e rótulos
                ax.set_title(f'Gráfico de Linhas: {tipo_aggregacao} de {eixo_y} por {eixo_x}', fontsize=16)
                ax.set_xlabel(eixo_x, fontsize=14)
                ax.set_ylabel(eixo_y, fontsize=14)

                # Melhorando a visualização
                plt.xticks(rotation=45)  # Girando rótulos do eixo x para melhor leitura
                ax.grid(True, linestyle='--', alpha=0.7)  # Adicionando uma grade com estilo

                # Adiciona a legenda
                ax.legend()

                # Ajustar automaticamente o layout para evitar que elementos fiquem fora da área visível
                plt.tight_layout()

                # Ocultando rótulos "0" ou "R$0,00"
                labels = [item.get_text() for item in ax.get_xticklabels()]
                labels = ['' if label in ['0', 'R$0,00'] else label for label in labels]
                ax.set_xticklabels(labels)

                # Exibindo o gráfico no Streamlit
                st.pyplot(figura)



        # Gráfico de Violino
        elif grafico_selecionado == "Gráfico de Violino":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)
            eixo_y = st.sidebar.selectbox("Selecione o eixo y", dados.columns)
            st.write("### Gráfico de Violino:")
            
            figura, ax = plt.subplots(figsize=(largura, altura))

            # Adicionando o gráfico de violino
            sns.violinplot(x=dados[eixo_x], y=dados[eixo_y], ax=ax, palette=paletas[paleta_escolhida], inner='box', linewidth=1.25)

            # Ajustando títulos e rótulos
            ax.set_title(f'Gráfico de Violino de {eixo_y} por {eixo_x}', fontsize=16)
            ax.set_xlabel(eixo_x, fontsize=14)
            ax.set_ylabel(eixo_y, fontsize=14)

            # Melhorando a visualização
            ax.grid(True, linestyle='--', alpha=0.7)  # Adicionando uma grade
            plt.xticks(rotation=45)  # Girando rótulos do eixo x para melhor leitura

            st.pyplot(figura)

        # Gráfico de Pizza
        elif grafico_selecionado == "Gráfico de Pizza":
            # Selecionar a coluna categórica
            coluna_categorica = st.sidebar.selectbox("Selecione a coluna categórica", dados.columns)

            # Opção para selecionar uma coluna de valores (opcional)
            coluna_valores = st.sidebar.selectbox("Selecione a coluna de valores (opcional)", [None] + list(dados.select_dtypes(['float64', 'int64']).columns))

            st.write("### Gráfico de Pizza:")

            figura, ax = plt.subplots(figsize=(largura, altura))

            if coluna_valores:  # Se uma coluna de valores for selecionada
                # Agrupar os dados pela coluna categórica e somar os valores correspondentes
                dados_pizza = dados.groupby(coluna_categorica)[coluna_valores].sum()
                # Verificar se a coluna de valores contém valores monetários (R$)
                is_monetary = "R$" in dados.columns or dados_pizza.max() > 1000  # Definição simples para detectar valores financeiros
            else:  # Se nenhuma coluna de valores for selecionada, usar a contagem de cada categoria
                dados_pizza = dados[coluna_categorica].value_counts()
                is_monetary = False  # Se estamos contando categorias, não há valores monetários

            # Usar uma paleta de cores
            cores = sns.color_palette(paletas[paleta_escolhida], len(dados_pizza))  # Ajuste a paleta conforme necessário

            # Função de formatação para exibir tanto % quanto valor (formatando se for monetário)
            def func_percent_valor(pct, valores):
                valor = int(pct / 100.0 * sum(valores))
                if is_monetary:
                    return f"{pct:.1f}%\nR${valor:,.0f}"  # Exibir o valor monetário formatado
                else:
                    return f"{pct:.1f}%\n{valor:,}"  # Exibir apenas o valor como quantidade

            # Criar o gráfico de pizza
            wedges, texts, autotexts = ax.pie(dados_pizza, 
                                            autopct=lambda pct: func_percent_valor(pct, dados_pizza),  # Chamar a função de formatação
                                            colors=cores, 
                                            startangle=90, 
                                            explode=[0.1] * len(dados_pizza),  # Destacar cada pedaço
                                            shadow=True, 
                                            wedgeprops={'edgecolor': 'w', 'linewidth': 0.5})  # Borda branca em cada fatia

            # Ajustar título e rótulos
            if coluna_valores:
                ax.set_title(f'Gráfico de Pizza de {coluna_categorica} (Baseado em {coluna_valores})', fontsize=16)
            else:
                ax.set_title(f'Gráfico de Pizza de {coluna_categorica}', fontsize=16)

            ax.set_ylabel('')  # Remover o rótulo do eixo Y para limpar o gráfico

            # Personalizar os textos das porcentagens
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(12)
                autotext.set_fontweight('bold')

            # Adicionar uma legenda fora do gráfico
            ax.legend(dados_pizza.index, title=coluna_categorica, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

            # Melhorando a visualização do gráfico
            ax.grid(False)  # Remover a grade
            plt.tight_layout()  # Ajuste para não cortar a legenda

            st.pyplot(figura)




 
        # Gráfico de Área
        elif grafico_selecionado == "Gráfico de Área":
            eixo_x = st.sidebar.selectbox("Selecione o eixo x", dados.columns)
            eixo_y = st.sidebar.selectbox("Selecione o eixo y", dados.columns)
            st.write("### Gráfico de Área:")
            
            figura, ax = plt.subplots(figsize=(largura, altura))

            # Verificar se a coluna eixo_y é numérica
            if dados[eixo_y].dtype not in [np.int64, np.float64]:
                st.warning(f"A coluna '{eixo_y}' contém valores não numéricos. Não é possível gerar o gráfico de área.")
            else:
                # Gerar o gráfico de área com estilo
                dados.plot.area(x=eixo_x, y=eixo_y, ax=ax, alpha=0.7)  # Ajusta a transparência
                ax.set_facecolor("#f7f7f7")  # Cor de fundo mais suave
                
                # Estilizando os rótulos e título
                ax.set_title(f'Gráfico de Área: {eixo_y} ao longo de {eixo_x}', fontsize=18, fontweight='bold')
                ax.set_xlabel(eixo_x, fontsize=14, fontweight='bold')
                ax.set_ylabel(eixo_y, fontsize=14, fontweight='bold')
                
                # Melhorar a visualização
                ax.grid(True, linestyle='--', alpha=0.5)  # Grade com estilo
                plt.xticks(rotation=45)  # Girar os rótulos do eixo X para melhor legibilidade

                st.pyplot(figura)


    else:
        st.warning("Nenhum dado carregado. Por favor, faça o upload de um arquivo CSV ou insira uma URL.")
if __name__ == "__main__":
    principal()
