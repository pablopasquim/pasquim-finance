import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

DATA_FILE = "data.json"

# ---------- Funções ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"salario": 0, "fixas": [], "variaveis": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ---------- Título ----------
st.set_page_config(page_title="Pasquim Finance", layout="centered")
st.title("💸 Pasquim Finance - Controle de Gastos")

# ---------- Salário ----------
st.header("1️⃣ Salário do mês")
salario = st.number_input("Informe seu salário mensal", value=data["salario"])
data["salario"] = salario

# ---------- Despesas Fixas ----------
st.header("2️⃣ Despesas Fixas")
with st.form("fixas_form"):
    nome_fixa = st.text_input("Nome da despesa fixa")
    valor_fixa = st.number_input("Valor da despesa", step=1.0)
    data_fixa = st.date_input("Data da despesa fixa", value=datetime.today())
    adicionar_fixa = st.form_submit_button("Adicionar despesa fixa")
    if adicionar_fixa and nome_fixa:
        data["fixas"].append({
            "nome": nome_fixa,
            "valor": valor_fixa,
            "data": data_fixa.strftime("%Y-%m-%d")
        })
        save_data(data)
        st.success(f"Despesa fixa '{nome_fixa}' adicionada!")

# Listar e remover fixas
if data["fixas"]:
    st.subheader("🧾 Lista de despesas fixas:")
    for i, item in enumerate(data["fixas"]):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"• {item['nome']} - R$ {item['valor']:.2f} em {item['data']}")
        with col2:
            if st.button("❌ Remover", key=f"remove_fixa_{i}"):
                data["fixas"].pop(i)
                save_data(data)
                st.experimental_rerun()

# ---------- Gastos Variáveis ----------
st.header("3️⃣ Gastos Variáveis")
with st.form("variaveis_form"):
    nome_var = st.text_input("Nome do gasto")
    valor_var = st.number_input("Valor do gasto", step=1.0, format="%.2f")
    categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Compras", "Outro"])
    data_var = st.date_input("Data do gasto", value=datetime.today())
    adicionar_var = st.form_submit_button("Registrar gasto")
    if adicionar_var and nome_var:
        data["variaveis"].append({
            "nome": nome_var,
            "valor": valor_var,
            "categoria": categoria,
            "data": data_var.strftime("%Y-%m-%d")
        })
        save_data(data)
        st.success(f"Gasto '{nome_var}' registrado com sucesso!")

# Listar e remover variáveis
if data["variaveis"]:
    st.subheader("🛒 Lista de gastos variáveis:")
    for i, item in enumerate(data["variaveis"]):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"• {item['nome']} - R$ {item['valor']:.2f} ({item['categoria']}) em {item['data']}")
        with col2:
            if st.button("❌ Remover", key=f"remove_var_{i}"):
                data["variaveis"].pop(i)
                save_data(data)
                st.experimental_rerun()

# ---------- Filtro por data ----------
st.header("📅 Filtro de gastos por data")
if data["variaveis"]:
    df_var = pd.DataFrame(data["variaveis"])
    df_var["data"] = pd.to_datetime(df_var["data"])

    start_date = st.date_input("Data inicial", value=df_var["data"].min().date())
    end_date = st.date_input("Data final", value=df_var["data"].max().date())

    filtro = df_var[(df_var["data"] >= pd.to_datetime(start_date)) & (df_var["data"] <= pd.to_datetime(end_date))]

    st.write("📋 Gastos filtrados:")
    st.dataframe(filtro[["data", "nome", "categoria", "valor"]])

    st.subheader("📊 Gráfico por categoria")
    st.bar_chart(filtro.groupby("categoria")["valor"].sum())

# ---------- Resumo ----------
total_fixas = sum([f["valor"] for f in data["fixas"]])
total_var = sum([v["valor"] for v in data["variaveis"]])
saldo = data["salario"] - total_fixas - total_var

st.header("💼 Resumo do mês")
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Salário", f"R$ {data['salario']:.2f}")
col2.metric("🧾 Fixas", f"R$ {total_fixas:.2f}")
col3.metric("🛒 Variáveis", f"R$ {total_var:.2f}")
col4.metric("✅ Saldo final", f"R$ {saldo:.2f}")
