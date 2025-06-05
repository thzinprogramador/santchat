import streamlit as st

st.set_page_config(page_title="SantChat", page_icon="🤖", layout="wide")

st.title("🤖 SantChat — Assistente IA do Banco")

st.write("Seja bem-vindo! Faça sua pergunta sobre processos internos, compliance, fluxos operacionais...")

# Caixa de texto para input do usuário
user_input = st.text_input("Digite sua pergunta:")

if user_input:
    st.write(f"🔍 Processando sua pergunta: **{user_input}**")

    # Aqui você coloca a lógica da IA
    # Exemplo básico com resposta fixa
    response = "🔐 Resposta simulada: Este processo exige validação dupla no sistema XYZ."

    st.success(response)
