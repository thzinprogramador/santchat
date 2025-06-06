import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Carrega a chave da API do arquivo .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="SantChat", page_icon="🤖", layout="wide")
st.title("🤖 SantChat — Assistente IA do Banco")
st.write("Seja bem-vindo! Faça sua pergunta sobre processos internos, compliance, fluxos operacionais...")

# Caixa de texto para input do usuário
user_input = st.text_input("Digite sua pergunta:")

def ask_groq(question):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "Você é o SantChat, uma IA treinada com manuais internos, normas de compliance e processos bancários. Responda sempre em tom profissional e adequado ao ambiente corporativo."},
            {"role": "user", "content": question}
        ],
        "model": "mixtral-8x7b-32768"
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "⚠️ Erro ao se conectar com a IA. Verifique sua chave e conexão."

if user_input:
    st.write(f"🔍 Processando sua pergunta: **{user_input}**")
    response = ask_groq(user_input)
    st.success(response)
