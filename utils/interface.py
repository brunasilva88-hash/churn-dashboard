import streamlit as st

def render_sidebar_usuario():    """Campo do nome na barra lateral, salvo na sessão (aparece em todas as páginas)."""    with st.sidebar:        st.markdown("---")        st.markdown("### 👤 Identificação")        st.text_input(            "Digite seu nome:",            key="nome_usuario",            placeholder="Seu nome aqui...",        )        st.markdown("---")        st.caption("📊 InsightData Analytics")    return st.session_state.get("nome_usuario", "")

def saudacao():    """Saudação personalizada no topo de cada página (menos a inicial)."""    nome = st.session_state.get("nome_usuario", "").strip()    if nome:        st.markdown(f"### 👋 Olá, **{nome}**! Que bom te ver por aqui.")    else:        st.info("💡 Digite seu nome na barra lateral para personalizar sua experiência.")    st.markdown("---")
