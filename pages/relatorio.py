import streamlit as st
import os
import json
import pandas as pd

st.title("📊 Relatórios e Comparativos")

arquivos = sorted([f for f in os.listdir("data") if f.endswith(".json")])
meses = [f.replace(".json", "") for f in arquivos]

df_data = []
for mes in meses:
    with open(f"data/{mes}.json", "r") as f:
        d = json.load(f)
    total_fixas = sum(i["valor"] for i in d.get("fixas", []))
    total_var = sum(i["valor"] for i in d.get("variaveis", []))
    total_parc = sum(i["valor"] for i in d.get("parcelas", []))
    total_cartao = 0
    for nome_cartao, cartao in d.get("cartoes", {}).items():
        total_cartao += cartao.get("gasto_atual", 0)
    total_gasto = total_fixas + total_var + total_parc
    saldo = d.get("salario", 0) - total_gasto
    df_data.append({
        "Mês": mes,
        "Salário": d.get("salario", 0),
        "Gasto Total": total_gasto,
        "Saldo": saldo,
        "Cartão": total_cartao
    })

df = pd.DataFrame(df_data)
st.dataframe(df)

st.bar_chart(df.set_index("Mês")["Gasto Total"])
st.line_chart(df.set_index("Mês")[["Salário", "Gasto Total"]])
