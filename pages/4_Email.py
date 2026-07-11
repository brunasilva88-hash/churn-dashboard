import streamlit as st
st.set_page_config(page_title="Enviar E-mail", page_icon="📧")

import smtplib
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def enviar_email(remetente_email, remetente_senha, destinatario, assunto, corpo, anexo_bytes=None, nome_anexo="grafico.png"):
    """Envia um e-mail via Gmail SMTP com ou sem anexo."""
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

# INTERFACE DA PÁGINA (o que aparece na tela)
st.title("📧 Enviar Relatório por E-mail")
st.write("Preencha os campos abaixo para enviar o e-mail com o anexo.")

remetente = st.text_input("📤 Seu e-mail (Gmail)")
senha = st.text_input("🔑 Senha de app do Gmail", type="password")
destinatario = st.text_input("📥 E-mail do destinatário")
assunto = st.text_input("✏️ Assunto", value="Relatório de Análise")
corpo = st.text_area("💬 Mensagem", value="Segue em anexo o relatório gerado.")

if st.button("Enviar E-mail 🚀"):
    if not remetente or not senha or not destinatario:
        st.warning("⚠️ Preencha o remetente, a senha e o destinatário!")
    else:
        try:
            enviar_email(
                remetente_email=remetente,
                remetente_senha=senha,
                destinatario=destinatario,
                assunto=assunto,
                corpo=corpo,
            )
            st.success("✅ E-mail enviado com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao enviar: {e}")                                                                                                 