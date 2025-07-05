# pages/cartao.py
import streamlit as st
import json
import os
from datetime import datetime

mes_atual = datetime.today().strftime("%Y-%m")
arquivo = f"data/{mes_atual}.json"

with open(arquivo, "r") as f:
    dados = json.load(f)

st.title("💳 Cartões de Crédito")

# Adicionar novo cartão
with st.form("add_card"):
    nome = st.text_input("Nome do cartão")
    limite = st.number_input("Limite total", step=10.0)
    if st.form_submit_button("Adicionar") and nome:
        dados["cartoes"][nome] = {"limite": limite, "gasto_atual": 0}
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
        st.success("Cartão adicionado com sucesso!")
        st.rerun()

# Exibir e editar cartões
for nome, info in dados["cartoes"].items():
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.write(f"**{nome}** - Limite: R$ {info['limite']:.2f}")
        st.progress(min(info['gasto_atual'] / info['limite'], 1.0))
        st.caption(f"Gasto atual: R$ {info['gasto_atual']:.2f}")
    with col2:
        novo_valor = st.number_input(f"Atualizar limite de {nome}", value=info['limite'], key=nome)
        if st.button("Atualizar limite", key=f"up_{nome}"):
            dados["cartoes"][nome]["limite"] = novo_valor
            with open(arquivo, "w") as f:
                json.dump(dados, f, indent=4)
            st.rerun()

    with col3:
        if st.button("Excluir", key=f"del_{nome}"):
            del dados["cartoes"][nome]
            with open(arquivo, "w") as f:
                json.dump(dados, f, indent=4)
            st.rerun()

