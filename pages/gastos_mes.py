# pages/gastos_mes.py
import streamlit as st
import json
import os
from datetime import datetime, date

mes_atual = datetime.today().strftime("%Y-%m")
arquivo = f"data/{mes_atual}.json"

with open(arquivo, "r") as f:
    dados = json.load(f)

def salvar():
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

st.title("💰 Gastos do Mês")

# Salário
st.subheader("Salário")
salario = st.number_input("Informe seu salário", value=dados["salario"])
dados["salario"] = salario
salvar()

# Despesas Fixas
st.subheader("Despesas Fixas")
with st.form("add_fixa"):
    nome_f = st.text_input("Nome da despesa fixa")
    valor_f = st.number_input("Valor", step=1.0)
    data_f = st.date_input("Data", value=date.today())
    if st.form_submit_button("Adicionar") and nome_f:
        dados["fixas"].append({"nome": nome_f, "valor": valor_f, "data": str(data_f)})
        salvar()
        st.rerun()


for i, item in enumerate(dados["fixas"]):
    st.write(f"{item['nome']} - R$ {item['valor']:.2f} em {item['data']}")
    if st.button("Remover fixa", key=f"rem_fixa_{i}"):
        dados["fixas"].pop(i)
        salvar()
        st.rerun()


# Gastos Variáveis
st.subheader("Gastos Variáveis")
with st.form("add_var"):
    nome_v = st.text_input("Nome do gasto")
    valor_v = st.number_input("Valor gasto", step=1.0, format="%.2f")
    forma = st.selectbox("Forma de pagamento", ["Débito", "Crédito", "Pix", "Dinheiro"])
    parcelas = 1
    if forma == "Crédito":
        parcelas = st.number_input("Parcelas", min_value=1, max_value=24, step=1)
        valor_p = st.number_input("Quantidade de parcelas", step=1.0, format="%.2f")
    data_v = st.date_input("Data do gasto", value=date.today())
    if st.form_submit_button("Adicionar gasto") and nome_v:
        if forma == "Crédito" and parcelas > 1:
            for p in range(parcelas):
                mes_futuro = datetime(data_v.year, data_v.month, 1).replace(month=(data_v.month + p - 1) % 12 + 1)
                mes_str = mes_futuro.strftime("%Y-%m")
                path = f"data/{mes_str}.json"
                if not os.path.exists(path):
                    with open(path, "w") as f:
                        f.write('{"salario": 0, "fixas": [], "variaveis": [], "parcelas": [], "cartoes": {}}')
                with open(path, "r") as f:
                    future_data = json.load(f)
                future_data["parcelas"].append({"nome": nome_v, "valor": valor_v/parcelas, "parcela": p+1, "de": parcelas})
                with open(path, "w") as f:
                    json.dump(future_data, f, indent=4)
        else:
            dados["variaveis"].append({"nome": nome_v, "valor": valor_v, "forma": forma, "data": str(data_v)})
            salvar()
        st.rerun()


for i, item in enumerate(dados["variaveis"]):
    st.write(f"{item['nome']} - R$ {item['valor']:.2f} via {item['forma']} em {item['data']}")
    if st.button("Remover gasto", key=f"rem_var_{i}"):
        dados["variaveis"].pop(i)
        salvar()
        st.rerun()


# Parcelas atuais
st.subheader("Parcelas neste mês")
for i, par in enumerate(dados.get("parcelas", [])):
    st.write(f"{par['nome']} - Parcela {par['parcela']}/{par['de']} - R$ {par['valor']:.2f}")
    if st.button("Remover parcela", key=f"rem_parc_{i}"):
        dados["parcelas"].pop(i)
        salvar()
        st.rerun()

