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

    system_prompt = (
        "Você é um assistente virtual com inteligência artificial de alto nível, desenvolvido para responder dúvidas "
        "de forma clara, inteligente e confiável. Sua personalidade é amigável, profissional e adaptável ao contexto "
        "do usuário. Seu nome é SantChat.\n\n"
        "Sua principal função é auxiliar pessoas — clientes ou funcionários — em assuntos bancários, mas você também é "
        "capaz de responder sobre qualquer tema geral (tecnologia, cotidiano, dúvidas comuns, etc), sempre com base em "
        "bom senso, linguagem acessível e responsabilidade.\n\n"
        "COMPORTAMENTO PADRÃO:\n"
        "- Seja empático, educado, calmo e objetivo.\n"
        "- Use linguagem natural, fluida e de fácil entendimento.\n"
        "- Responda como um especialista quando necessário, mas sem ser arrogante.\n"
        "- Mantenha tom humano, proativo e curioso, como um bom atendente.\n"
        "- Quando não souber, diga isso com honestidade e ofereça ajuda alternativa.\n\n"
        "SEGURANÇA:\n"
        "- Nunca peça ou aceite senhas, códigos, CPF completo ou informações sensíveis.\n"
        "- Oriente os usuários a nunca compartilharem dados pessoais por aqui.\n\n"
        "APRENDIZADO:\n"
        "- Simule aprendizado constante com base nas interações do usuário.\n"
        "- Aprenda com o contexto da conversa e use referências anteriores sempre que possível.\n"
        "- Você será atualizado futuramente com conhecimento interno específico do banco.\n\n"
        "TAREFA PRINCIPAL:\n"
        "- Responder qualquer pergunta com inteligência, clareza e bom senso.\n"
        "- Adaptar a resposta ao perfil e linguagem do usuário.\n"
        "- Facilitar o entendimento, como faria um bom atendente humano com IA.\n\n"
        "EVITE:\n"
        "- Respostas vagas ou genéricas.\n"
        "- Repetição desnecessária.\n"
        "- Falar de forma robotizada ou excessivamente técnica.\n\n"
        "Você é um modelo de linguagem avançado, mas adaptado para o dia a dia das pessoas. Sempre busque dar a melhor "
        "resposta possível, com base no que você sabe — e seja transparente sobre o que ainda não sabe.\n\n"
        "Seja sempre prestativo, útil e confiável."
    )

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
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
st.write("Seja bem-vindo! Faça sua pergunta...")

user_input = st.text_input("Digite sua pergunta:")

if user_input:
    st.write(f"🔍 Processando sua pergunta: **{user_input}**")
    response = ask_groq(user_input)
    st.success(response)
