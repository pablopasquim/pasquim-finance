# pages/historico.py
import streamlit as st
import json
import os

st.title("📂 Histórico de Meses")

arquivos = sorted([f for f in os.listdir("data") if f.endswith(".json")])
meses = [f.replace(".json", "") for f in arquivos]

escolhido = st.selectbox("Escolha o mês para visualizar", meses[::-1])

with open(f"data/{escolhido}.json", "r") as f:
    dados = json.load(f)

st.subheader(f"Salário em {escolhido}: R$ {dados['salario']:.2f}")

st.write("### Fixas")
for item in dados["fixas"]:
    st.write(f"{item['nome']} - R$ {item['valor']:.2f} em {item['data']}")

st.write("### Variáveis")
for item in dados["variaveis"]:
    st.write(f"{item['nome']} - R$ {item['valor']:.2f} via {item['forma']} em {item['data']}")

st.write("### Parcelas")
for par in dados["parcelas"]:
    st.write(f"{par['nome']} - Parcela {par['parcela']}/{par['de']} - R$ {par['valor']:.2f}")

st.write("### Cartões")
for nome, cartao in dados.get("cartoes", {}).items():
    st.write(f"Cartão {nome}: Gasto R$ {cartao['gasto_atual']:.2f} de R$ {cartao['limite']:.2f}")
