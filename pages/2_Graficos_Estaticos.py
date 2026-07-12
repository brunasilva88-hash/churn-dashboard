import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Graficos Estaticos", layout="wide")
st.title("Graficos Estaticos")
st.markdown("Visualizacoes gerais sobre o perfil dos clientes e o comportamento de churn.")
st.divider()

@st.cache_data
def carregar_dados():
        df = pd.read_csv("data/telco_churn.csv")
        return df
df = carregar_dados()

st.subheader("1. Distribuicao de Churn")

churn_col = None
for col in ["Churn Label", "Churn", "churn", "churn_label"]:
    if col in df.columns:
        churn_col = col
        break

if churn_col:
    col1, col2 = st.columns(2)

    with col1:
     contagem_churn = df[churn_col].value_counts().reset_index()
     contagem_churn.columns = ["Status", "Quantidade"]    
     fig_pizza = px.pie(
            contagem_churn,
            names="Status",
            values="Quantidade",
            title="Distribuição de Churn",
            color_discrete_sequence=["#2ecc71", "#e74c3c"]
        )
     st.plotly_chart(fig_pizza, use_container_width=True)

    with col2:
        fig_barra = px.bar(
                contagem_churn,
                x="Status",
                y="Quantidade",
                title="Quantidade por Status de Churn",
                color="Status",
                color_discrete_sequence=["#2ecc71", "#e74c3c"],
                text="Quantidade"
            )
        fig_barra.update_traces(textposition="outside")        
        st.plotly_chart(fig_barra, use_container_width=True)
else:
    st.warning("Coluna de Churn nao encontrada no dataset.")

st.divider()

st.subheader("2. Perfil dos Clientes")

col3, col4 = st.columns(2)

with col3:
    if "Gender" in df.columns:
        genero = df["Gender"].value_counts().reset_index()
        genero.columns = ["Gênero", "Quantidade"]
        fig_genero = px.bar(
            genero,
            x="Gênero",
            y="Quantidade",
            title="Distribuição por Gênero",
            color="Gênero",
            color_discrete_sequence=["#3498db", "#e91e8c"],
            text="Quantidade"
        )
        fig_genero.update_traces(textposition="outside")
        fig_genero.update_layout(
            yaxis=dict(
                range=[3400, 3600],
                title="Quantidade"
            )
        )                                          
        st.plotly_chart(fig_genero, use_container_width=True)

with col4:
    if "Age" in df.columns:
        fig_idade = px.histogram(
            df,
            x="Age",
            nbins=30,
            title="Distribuição de idade dos Clientes",
            color_discrete_sequence=["#9b59b6"]
        )
        fig_idade.update_layout(bargap=0.1)
        st.plotly_chart(fig_idade, use_container_width=True)

st.divider()

st.subheader("3. Tipo de Contrato")

col5, col6 = st.columns(2)

with col5:
    if "Contract" in df.columns:
        contrato = df["Contract"].value_counts().reset_index()
        contrato.columns = ["Tipo", "Quantidade"]
        fig_contrato = px.pie(
            contrato,
            names="Tipo",
            values="Quantidade",
            title="Distribuição por Tipo de Contrato",
            color_discrete_sequence=["#f39c12", "#1abc9c", "#e74c3c"],
        )
        st.plotly_chart(fig_contrato, use_container_width=True)

with col6:
    if churn_col and "Gender" in df.columns:
        churn_genero = df.groupby(["Gender", churn_col]).size().reset_index(name="Quantidade")
        fig_churn_genero = px.bar(
            churn_genero,
            x="Gender",
            y="Quantidade",
            color=churn_col,
            title="Churn por Gênero",
            barmode="group",
            color_discrete_sequence=["#2ecc71", "#e74c3c"],
        )
        st.plotly_chart(fig_churn_genero, use_container_width=True)

st.divider()

st.subheader("4. Receita Mensal")

receita_col = None
for col in ["Monthly Charge", "MonthlyCharges", "Monthly Charges", "monthly_charges"]:
    if col in df.columns:
        receita_col = col
        break

if receita_col and churn_col:
    fig_receita = px.box(
        df,
        x=churn_col,
        y=receita_col,
        title="Receita Mensal por Status de Churn",
        color=churn_col,
        color_discrete_sequence=["#2ecc71", "#e74c3c"],
    )
    st.plotly_chart(fig_receita, use_container_width=True)    
elif receita_col:
    fig_receita2 = px.histogram(
        df,
        x=receita_col,
        nbins=40,
        title="Distribuição da Receita Mensal",
        color_discrete_sequence=["#f39c12"],
    )
    st.plotly_chart(fig_receita2, use_container_width=True)
else:
    st.info("Coluna de receita nao encontrada no dataset.")                    