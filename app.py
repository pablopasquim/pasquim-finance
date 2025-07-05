import streamlit as st
from datetime import datetime
import os

# Páginas
st.set_page_config(page_title="Pasquim Finance", layout="wide")
st.title("💸 Pasquim Finance")

st.write("Bem-vinda ao seu gerenciador financeiro, Raque🥰! Use o menu lateral para navegar entre as funcionalidades.")

# Verifica se a pasta de dados existe
if not os.path.exists("data"):
    os.makedirs("data")

# Cria o arquivo do mês atual, se não existir
mes_atual = datetime.today().strftime("%Y-%m")
path_arquivo_mes = f"data/{mes_atual}.json"
if not os.path.exists(path_arquivo_mes):
    with open(path_arquivo_mes, "w") as f:
        f.write('{"salario": 0, "fixas": [], "variaveis": [], "parcelas": [], "cartoes": {}}')

st.success(f"Mês atual carregado: {mes_atual}")