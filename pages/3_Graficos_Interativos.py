import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Graficos Interativos", page_icon="🎛️", layout="wide")

st.title("🎛️ Graficos Interativos")
st.markdown("Use os filtros na barra lateral para explorar os dados")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/telco_churn.csv")
    return df

df = carregar_dados()

st.sidebar.header("🔎 Filtros")

if "Gender" in df.columns:
    generos = st.sidebar.multiselect(
        "Gênero:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()        
    )
else:
    generos = None

if "Contract" in df.columns:
    contratos = st.sidebar.multiselect(
        "Tipo de Contrato:",
        options=df["Contract"].unique(),
        default=df["Contract"].unique()        
    )
else:
    contratos = None

df_filtrado = df.copy()

if generos is not None:
    df_filtrado = df_filtrado[df_filtrado["Gender"].isin(generos)]

if contratos is not None:
    df_filtrado = df_filtrado[df_filtrado["Contract"].isin(contratos)]

st.metric("👥 Clientes filtrados", len(df_filtrado))

if "Churn" in df_filtrado.columns:
    churn_data = df_filtrado["Churn"].value_counts().reset_index()
    churn_data.columns = ["Churn", "Quantidade"]
    fig_churn = px.bar(
        churn_data,
        x="Churn",
        y="Quantidade",
        title="Distribuição de Churn (Filtrado)",
         color="Churn Label",
        color_discrete_sequence=["#2ecc71", "#e74c3c"],
        text="Quantidade"
    )
    fig_churn.update_traces(textposition="outside")
    st.plotly_chart(fig_churn, use_container_width=True)

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# GRAFICO 1: Box Plot - Receita Mensal por Genero e Churn

if "Monthly Charge" in df_filtrado.columns and "Gender" in df_filtrado.columns:
    fig_box = px.box(
        df_filtrado,
        x="Gender",
        y="Monthly Charge",
        color="Churn Label",
        title="Receita Mensal por Gênero e Churn",
        color_discrete_map={"Yes": "#e74c3c", "No": "#2ecc71"},
        points=False,
    )
    fig_box.update_layout(
        legend_title_text="Churn",
        xaxis_title="Gênero",
        yaxis_title="Receita Mensal",
    )
    st.plotly_chart(fig_box, use_container_width=True)

# GRAFICO 2: Violin Plot - Tempo de Permanencia por Churn e Genero

if "Tenure in Months" in df_filtrado.columns:
    fig_violin = px.violin(
        df_filtrado,
        x="Churn Label",
        y="Tenure in Months",
        color="Gender",
        box=True,
        title="Tempo de Permanencia por Churn e Genero",
        color_discrete_map={"Male": "#3498db", "Female": "#e91e63"},
        labels={
            "Churn Label": "Churn",
            "Tenure in Months": "Tempo de Permanencia (Meses)",
            "Gender": "Gênero",
        },
    )
    st.plotly_chart(fig_violin, use_container_width=True)

# GRAFICO 3: Heatmap de Contagem - Genero x Churn

if "Gender" in df_filtrado.columns and "Churn Label" in df_filtrado.columns:
    df_heatmap = (
        df_filtrado
        .groupby(["Gender", "Churn Label"])
        .size()
        .reset_index(name="Quantidade")
    )

    fig_heat = px.density_heatmap(
        df_heatmap,
        x="Churn Label",
        y="Gender",
        z="Quantidade",
        text_auto=True,
        title="Contagem de Clientes: Genero x Churn",
        color_continuous_scale="RdYlGn_r",
    )
    fig_heat.update_traces(textfont_size=16)
    st.plotly_chart(fig_heat, use_container_width=True)    




