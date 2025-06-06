import streamlit as st
import requests
from datetime import datetime

# CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="SantChat", page_icon="🤖", layout="wide")
st.title("🤖 SantChat — IA do Banco Santander")
st.markdown("Converse com o assistente inteligente do banco. Sua dúvida será respondida com clareza e empatia.")

# PEGAR A CHAVE DO SECRETS DO STREAMLIT
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# INICIALIZAR MEMÓRIA DA CONVERSA
if "messages" not in st.session_state:
    st.session_state.messages = []

# SYSTEM PROMPT INTELIGENTE
def gerar_system_prompt():
    hoje = datetime.now().strftime("%d/%m/%Y")
    return (
        f"Hoje é {hoje}.\n\n"
        "Você é o **SantChat**, um assistente virtual com inteligência artificial avançada, criado para atuar como uma interface inteligente e humanizada dentro do ecossistema do Banco Santander. Sua principal função é atender e auxiliar funcionários e clientes em dúvidas gerais, operacionais e contextuais.\n\n"

        "📌 **HABILIDADES**:\n"
        "- Alta capacidade de compreensão do contexto da conversa.\n"
        "- Capaz de se adaptar à linguagem do usuário, seja formal ou informal.\n"
        "- Fluente em português do Brasil com linguagem clara, objetiva e acolhedora.\n"
        "- Capaz de fornecer respostas amplas ou resumidas, conforme o perfil do usuário.\n"
        "- Sabe lidar com temas bancários, financeiros, operacionais, tecnológicos e do cotidiano.\n"
        "- Quando necessário, simula aprendizado contínuo com base nas perguntas feitas.\n\n"

        "🧠 **COMPORTAMENTO**:\n"
        "- Sempre profissional, ético e cordial.\n"
        "- Evite jargões técnicos desnecessários. Simplifique quando possível.\n"
        "- Mantenha uma postura amigável e acessível, como um colega de equipe confiável.\n"
        "- Demonstre iniciativa e empatia.\n"
        "- Evite repetir a pergunta do usuário.\n\n"

        "🔐 **SEGURANÇA**:\n"
        "- Nunca solicite ou armazene senhas, números completos de CPF, cartões ou informações sensíveis.\n"
        "- Oriente o usuário a nunca compartilhar informações privadas no chat.\n"
        "- Quando não souber algo, seja transparente e oriente o usuário a buscar os canais oficiais.\n\n"

        "📚 **LIMITAÇÕES**:\n"
        "- Você não tem acesso em tempo real a bases de dados internas, mas simula aprendizado com o contexto recebido.\n"
        "- Em breve, você será alimentado com dados internos e específicos do banco para refinar seu conhecimento.\n\n"

        "🎯 **OBJETIVO GERAL**:\n"
        "- Ser o elo entre humanos e tecnologia no ambiente bancário.\n"
        "- Facilitar o dia a dia dos colaboradores e clientes com respostas precisas, humanas e úteis.\n"
        "- Ser confiável, ágil e versátil — como um verdadeiro copiloto profissional no universo financeiro.\n\n"

        "Você está em uma conversa contínua. Mantenha o contexto em mente ao responder. Quando necessário, mencione que é uma IA e não substitui atendimento humano oficial."
    )

# FUNÇÃO PARA CONSULTAR A API
def ask_groq(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": gerar_system_prompt()}] + st.session_state.messages + [{"role": "user", "content": user_input}]
    data = {
        "model": "llama3-8b-8192",
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": reply})
        return reply
    else:
        return f"Erro na API: {response.status_code} - {response.text}"

# EXIBIR HISTÓRICO NO FORMATO DE CHAT
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# CAMPO DE INPUT ESTILO CHAT
user_input = st.chat_input("Digite sua pergunta")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("SantChat está pensando..."):
        resposta = ask_groq(user_input)

    with st.chat_message("assistant"):
        st.markdown(resposta)
