import streamlit as st
import requests
import json

# ==========================================
# 1. CONFIGURACIÓN Y ESTILO QUANTUM
# ==========================================
st.set_page_config(page_title="Quantum Life Architect", page_icon="🧬", layout="wide")

def style_architect():
    st.markdown("""
        <style>
        .main { background-color: #05070a; }
        [data-testid="stSidebar"] { background-color: #0b0e14; border-right: 1px solid #1f2937; }
        .stChatMessage { border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 10px; }
        </style>
        """, unsafe_allow_html=True)

style_architect()

# ==========================================
# 2. CONEXIÓN NEURONAL (DeepSeek)
# ==========================================
API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = st.secrets["DEEPSEEK_API_KEY"]

def consultar_deepseek(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": messages
    }
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# ==========================================
# 3. ESTADO DE SESIÓN
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 4. INTERFAZ DE CONSULTORÍA
# ==========================================
st.title("🏛️ Quantum Life Architect")

# Mostrar historial completo
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 5. CEREBRO DEL ARCHITECT (con historial)
# ==========================================
if prompt := st.chat_input("Describe un síntoma o un objetivo de vida..."):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Arquitectando respuesta..."):
            try:
                # Pasamos TODO el historial a DeepSeek
                res_text = consultar_deepseek(st.session_state.messages)
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"Error de conexión: {e}")
