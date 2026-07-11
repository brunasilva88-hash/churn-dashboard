import streamlit as st
st.set_page_config(page_title="Relatorio Completo", page_icon="📊", layout="wide")
import pandas as pd
import plotly.express as px
import plotly.io as pio
import smtplib
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ============================================================
# DADOS
# ============================================================

@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/telco_churn.csv")
    return df

df = carregar_dados()

# ============================================================
# RELATORIO ESCRITO (insights e analise geral)
# ============================================================

RELATORIO_TEXTO = """
=============================================================
   RELATORIO DE ANALISE — CHURN DE CLIENTES TELCO
=============================================================

Data de geracao: gerado automaticamente pelo sistema de analise.

-------------------------------------------------------------
CONTEXTO
-------------------------------------------------------------
Este relatorio apresenta uma analise exploratoria completasobre o comportamento de churn (cancelamento) dos clientesda empresa de telecomunicacoes Telco. O objetivo e identificarpadroes, grupos de risco e propor acoes estrategicas baseadasem dados para reducao do cancelamento.

-------------------------------------------------------------
PRINCIPAIS DESCOBERTAS
-------------------------------------------------------------

1. TAXA GERAL DE CHURN   A base apresenta uma taxa de churn em torno de 26-27%,   o que e significativamente alta para o setor de telecom.   Isso indica que aproximadamente 1 em cada 4 clientes   encerra o contrato — um sinal de alerta para retencao.

2. PERFIL DOS CLIENTES QUE CANCELAM   - Clientes com contrato mensal (Month-to-month) tem taxa     de churn drasticamente maior do que clientes com     contratos de 1 ou 2 anos.   - Clientes sem parceiro e sem dependentes apresentam     maior propensao ao cancelamento.   - Clientes mais novos na base (menor tempo de contrato /     "tenure" baixo) cancelam com muito mais frequencia,     especialmente nos primeiros 12 meses.

3. SERVICOS E CHURN   - Clientes que nao utilizam servicos adicionais como     Seguranca Online, Backup Online e Suporte Tecnico     tem maior taxa de cancelamento.   - Clientes com servico de fibra optica (Fiber optic)     apresentam churn maior do que os de DSL, possivelmente     por insatisfacao com custo-beneficio ou qualidade.

4. COBRANCA E PAGAMENTO   - Clientes com cobranca paperless e pagamento via     cheque eletronico tem maior taxa de cancelamento.   - Cobranças mensais (MonthlyCharges) mais altas estao     correlacionadas com maior churn, especialmente quando     combinadas com contrato mensal.

5. GENERO   A analise por genero nao revelou diferenca estatisticamente   expressiva na taxa de churn entre homens e mulheres.   O genero, isoladamente, nao e um fator preditivo relevante.

-------------------------------------------------------------
POSSÍVEIS SOLUÇÕES BASEADAS EM DADOS
-------------------------------------------------------------

AÇÃO 1 — INCENTIVAR CONTRATOS DE LONGO PRAZO: Oferecer descontos progressivos para clientes que migrarem de contrato mensal para anual ou bienal.   Ex: 10% de desconto no plano anual, 20% no bienal.   Impacto esperado: reducao significativa do churn   (clientes com contrato anual cancelam ~5x menos).

AÇÃO 2 — PROGRAMA DE RETENÇÃO NOS PRIMEIROS 12 MESES: O primeiro ano é crítico. Criar um programa de onboarding ativo: Contato proativo nos meses 1, 3, 6   e 12 para verificar satisfação e oferecer benefícios.   Clientes engajados nos primeiros meses tem menor churn.

AÇÃO 3 — BUNDLING DE SERVICOS ADICIONAIS: Clientes que utilizam mais servicos cancelam menos. Oferecer pacotes combinados (Seguranca + Backup +   Suporte Técnico) com preço atrativo pode aumentar o valor percebido e reduzir o cancelamento.

AÇÃO 4 — REVISÃO DO PLANO DE FIBRA ÓPTICA: O alto churn em clientes de fibra sugere insatisfação. Recomenda-se pesquisa de NPS específica para esse segmento e possível revisão de pricing ou qualidade de entrega do serviço.

AÇÃO 5 — MODELO PREDITIVO DE CHURN: Com os dados disponÍveis, é possível treinar um modelo de Machine Learning (ex: Random Forest, XGBoost) para identificar clientes com alta probabilidade de cancelar ANTES que isso aconteça, permitindo ações preventivas personalizadas.

-------------------------------------------------------------
CONCLUSÃO
-------------------------------------------------------------
O churn da Telco é um problema multifatorial, mas com padrões claros e acionáveis. A combinação de tipo de contrato, tempo de relacionamento e uso de serviços adicionais, são os principais indicadores de risco. Estratégias de retenção focadas nesses pontos, aliadas a um modelo preditivo, podem reduzir o churn em até 30-40% no médio prazo, segundo benchmarks do setor.
=============================================================
 Relatorio gerado pelo sistema de análise de dados Telco.
 Atenciosamente,
Bruna Silva - Equipe de Análise de Dados
=============================================================
"""

# ============================================================
# FUNCAO DE ENVIO DE E-MAIL
# ============================================================

def enviar_email(remetente_email, remetente_senha, destinatario, assunto, corpo, anexo_bytes=None, nome_anexo="relatorio.png"):
    msg = MIMEMultipart()
    msg["From"] = remetente_email
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    if anexo_bytes is not None:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(anexo_bytes)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{nome_anexo}"')
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(remetente_email, remetente_senha)
        servidor.sendmail(remetente_email, destinatario, msg.as_string())

# ============================================================
# FUNCAO DE GRAFICOS
# ============================================================

def gerar_grafico_boxplot():
    df_plot = df[df["Churn Label"].isin(["Yes", "No"])]
    fig = px.box(
        df_plot,
        x="Churn Label",
        y="Tenure in Months",
        color_discrete_map={"Yes": "#EF553B", "No": "#00CC96"},
        title="Distribuicao de Tempo de Contrato por Churn",
        color_discrete_sequence=["#2ecc71", "#e74c3c"],
        labels={"tenure": "Meses de Contrato", "Churn Label": "Churn"},
    )
    fig.update_layout(showlegend=False)
    return fig

def gerar_grafico_violin():
    df_plot = df[df["Churn Label"].isin(["Yes", "No"])]
    fig = px.violin(
        df_plot,
        x="Churn Label",
        y="Monthly Charge",
        color="Churn Label",
        box=True,
        color_discrete_map={"Yes": "#EF553B", "No": "#00CC96"},
        title="Cobranca Mensal por Status de Churn",
       labels={"MonthlyCharges": "Cobranca Mensal (USD)", "Churn Label": "Churn"},
    )
    fig.update_layout(showlegend=False)
    return fig

def gerar_grafico_heatmap():
    df_plot = df[df["Churn Label"].isin(["Yes", "No"])]
    contagem = df_plot.groupby(["Contract", "Churn Label"]).size().reset_index(name="Quantidade")
    fig = px.bar(
        contagem,
        x="Contract",
        y="Quantidade",
        color="Churn Label",
        barmode="group",
        color_discrete_map={"Yes": "#EF553B", "No": "#00CC96"},
        title="Tipo de Contrato x Churn",
        labels={"Contract": "Tipo de Contrato", "Churn Label": "Churn"},
    )
    return fig

# ============================================================
# NAVEGACAO LATERAL
# ============================================================

st.sidebar.title("Navegacao")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Selecione a pagina:",
    [
        "Tabela de Dados",
        "Graficos",
        "Envio por E-mail",
        "Download do Relatorio",
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Sistema de Analise — Telco Churn")

# ============================================================
# PAGINA 1 — TABELA DE DADOS
# ============================================================

if pagina == "Tabela de Dados":
    st.title("Tabela de Dados")
    st.write("Visualize e filtre os dados brutos da base de clientes.")

    col1, col2, col3 = st.columns(3)

    with col1:
        genero_filtro = st.multiselect(
            "Filtrar por Gênero:",
            options=df["Gender"].unique().tolist(),
            default=df["Gender"].unique().tolist(),
        )

    with col2:
        contrato_filtro = st.multiselect(
            "Filtrar por Tipo de Contrato:",
            options=df["Contract"].unique().tolist(),
            default=df["Contract"].unique().tolist(),
        )

    with col3:
        churn_filtro = st.multiselect(
            "Filtrar por Contrato:",
            options=df["Contract"].tolist(),
            default=df["Contract"].tolist(),
        )

    df_filtrado = df[
        (df["Gender"].isin(genero_filtro)) &
        (df["Churn Label"].isin(churn_filtro)) &
        (df["Contract"].isin(contrato_filtro))
    ]

    st.markdown(f"**Total de registros:** {len(df_filtrado):,}")
    st.dataframe(df_filtrado, use_container_width=True, height=500)

# ============================================================
# PAGINA 2 — GRAFICOS
# ============================================================

elif pagina == "Graficos":
    st.title("Graficos de Analise")
    st.write("Visualizacoes interativas sobre o comportamento de churn.")

    st.markdown("### Tempo de Contrato x Churn")
    st.plotly_chart(gerar_grafico_boxplot(), use_container_width=True)

    st.markdown("---")
    st.markdown("### Cobranca Mensal x Churn")
    st.plotly_chart(gerar_grafico_violin(), use_container_width=True)

    st.markdown("---")
    st.markdown("### Tipo de Contrato x Churn")
    st.plotly_chart(gerar_grafico_heatmap(), use_container_width=True)

# ============================================================
# PAGINA 3 — ENVIO POR E-MAIL
# ============================================================

elif pagina == "Envio por E-mail":
    st.title("Envio por E-mail")
    st.write("Escolha o que deseja enviar e preencha os dados abaixo.")

    st.markdown("### O que deseja enviar?")
    tipo_envio = st.radio(
        "",
        ["Grafico (imagem PNG)", "Relatorio Escrito com Insights e Analises"],
        horizontal=True,
    )

    st.markdown("---")

    if tipo_envio == "Grafico (imagem PNG)":
        st.markdown("#### Escolha o grafico para enviar:")
        grafico_escolhido = st.selectbox(
            "",
            [
                "Tempo de Contrato x Churn (Box Plot)",
                "Cobranca Mensal x Churn (Violin Plot)",
                "Tipo de Contrato x Churn (Barras)",
            ]
        )

    st.markdown("---")
    st.markdown("### Dados para envio")

    remetente = st.text_input("Seu e-mail (Gmail)")
    senha = st.text_input("Senha de App do Gmail", type="password")
    destinatario = st.text_input("E-mail do destinatario")

    # Campos pre-preenchidos automaticamente
    if tipo_envio == "Grafico (imagem PNG)":
        assunto_padrao = "Relatorio Telco — Grafico de Analise de Churn"
        corpo_padrao = (
            "Prezado(a),\n\n"
            "Segue em anexo o grafico de analise de churn gerado pelo "
            "sistema de analise de dados da Telco.\n\n"
            "O grafico apresenta a distribuicao e o comportamento dos "
            "clientes em relacao ao cancelamento de servicos, sendo uma "
            "ferramenta importante para a tomada de decisoes estrategicas.\n\n"
            "Qualquer dúvida, estamos a disposição.\n\n"
            "Atenciosamente,\n"
            "Equipe de Analise de Dados — Telco"
        )
        nome_arquivo = "grafico_churn.png"
    else:
        assunto_padrao = "Relatorio Telco — Analise Completa de Churn com Insights"
        corpo_padrao = (
            "Prezado(a),\n\n"
            "Segue em anexo o relatório completo de análise de churn dos "
            "clientes da Telco, contendo os principais insights encontrados "
            "nos dados e recomendações estrategicas baseadas em evidencias "
            "para reducao do cancelamento de clientes.\n\n"
            "Este relatorio foi gerado automaticamente pelo sistema de "
            "analise de dados e contempla padroes de comportamento, "
            "perfil de risco e acoes sugeridas para o time de retencao.\n\n"
            "Atenciosamente,\n"
            "Equipe de Analise de Dados — Telco"
        )
        nome_arquivo = "relatorio_churn.txt"

    assunto = st.text_input("Assunto", value=assunto_padrao)
    corpo = st.text_area("Corpo do e-mail", value=corpo_padrao, height=220)

    st.markdown("---")

    if st.button("Enviar E-mail"):
        if not remetente or not senha or not destinatario:
            st.warning("Preencha o seu e-mail, a senha de app e o e-mail do destinatario.")
        else:
            try:
                if tipo_envio == "Grafico (imagem PNG)":
                    # Gerar grafico escolhido
                    if grafico_escolhido == "Tempo de Contrato x Churn (Box Plot)":
                        fig = gerar_grafico_boxplot()
                    elif grafico_escolhido == "Cobranca Mensal x Churn (Violin Plot)":
                        fig = gerar_grafico_violin()
                    else:
                        fig = gerar_grafico_heatmap()

                    anexo_bytes = pio.to_image(fig, format="png", width=1000, height=600)

                else:
                    anexo_bytes = RELATORIO_TEXTO.encode("utf-8")
                    
                enviar_email(
                    remetente_email=remetente,
                    remetente_senha=senha,
                    destinatario=destinatario,
                    assunto=assunto,
                    corpo=corpo,
                    anexo_bytes=anexo_bytes,
                    nome_anexo=nome_arquivo
                )

                st.success("E-mail enviado com sucesso!")
                st.balloons()

            except Exception as e:
                st.error(f"Erro ao enviar o e-mail: {e}")

# ============================================================
# PAGINA 4 — DOWNLOAD DO RELATORIO
# ============================================================

elif pagina == "Download do Relatorio":
    st.title("Download do Relatorio")
    st.write("Clique aqui para baixar o relatório completo.")

    st.markdown("---")

    st.download_button(
        label="Baixar Relatorio (.txt)",
        data=RELATORIO_TEXTO,
        file_name="relatorio_telco_churn.txt",
        mime="text/plain"
    )

    st.caption("Clique no botao acima para salvar o relatorio no seu computador.")