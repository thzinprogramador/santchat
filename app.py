import streamlit as st
import requests

# PEGAR A CHAVE DO STREAMLIT SECRETS
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def ask_groq(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "Você é um assistente bancário. Responda com precisão e profissionalismo."},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Erro na API: {response.status_code} - {response.text}"

# --- APP STREAMLIT ---
st.set_page_config(page_title="SantChat", page_icon="🤖", layout="wide")
st.title("🤖 SantChat — Assistente IA do Banco")
st.write("Seja bem-vindo! Faça sua pergunta sobre processos internos, compliance, fluxos operacionais...")

user_input = st.text_input("Digite sua pergunta:")

if user_input:
    st.write(f"🔍 Processando sua pergunta: **{user_input}**")
    response = ask_groq(user_input)
    st.success(response)
