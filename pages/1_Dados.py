import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dados", page_icon="📋", layout="wide")

st.title("📋 Base de Clientes")

df = pd.read_csv("data/telco_churn.csv")

st.success(f"✅ Dados carregados! {df.shape[0]} clientes e {df.shape[1]} colunas.")

st.markdown("### 👀 Visualização dos dados")
st.dataframe(df, use_container_width=True)