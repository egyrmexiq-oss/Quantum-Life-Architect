import streamlit as st
import requests
import streamlit.components.v1 as components
import json
import os

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
# 4. INTERFAZ DE CONSULTORÍA
# ==========================================
st.title("🏛️ Quantum Life Architect")
st.caption(f"Diseñando tu mejor versión a los {edad} años • Enfoque: {foco}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Historial de Consultoría
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 5. CEREBRO DEL ARCHITECT
# ==========================================
if prompt := st.chat_input("Describe un síntoma o un objetivo de vida..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Arquitectando respuesta..."):
            sintomas_str = ", ".join(st.session_state.get('sintomas_reportados', []))
            
            contexto_filosofico = f"""
            Eres el 'Quantum Life Architect'. Tu misión es rediseñar la vitalidad del usuario.
            PERFIL BIOLÓGICO:
            - Género: {genero}
            - Edad: {edad} años
            - Enfoque prioritario: {foco}
            - Síntomas actuales: {sintomas_str if sintomas_str else 'Ninguno reportado'}
            FILOSOFÍA QUANTUM:
            - La edad es un dato, no un destino.
            - El gatillo del envejecimiento es la ignorancia, no el tiempo.
            - La mejora es posible en cualquier etapa si el diseño es correcto.
            DIRECTIVAS DE RESPUESTA:
            - Usa la biología de su género ({genero}) para dar consejos precisos.
            - Desmitifica que sus síntomas sean "normales por la edad".
            - Propón 3 acciones de arquitectura de vida.
            - Sugiere Quantum Mind o Supplements si el caso lo requiere.
            """

            try:
                res_text = consultar_deepseek([
                    {"role": "system", "content": contexto_filosofico},
                    {"role": "user", "content": prompt}
                ])
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"Error de conexión: {e}")

    if st.session_state.get('solicitar_plan'):
        with st.chat_message("assistant", avatar="🏛️"):
            with st.spinner("Diseñando tu Plan Maestro de Longevidad..."):
                historial = str(st.session_state.messages)
            prompt_plan = f"""
            Basado en nuestra consultoría: {historial}.
            Genera un 'Plan Maestro de Longevidad Quantum' con:
            1. Diagnóstico de Hábitos Actuales.
            2. Protocolo de Acción (Mañana, Tarde, Noche).
            3. Sugerencia de Expertos.
            """
            try:
                res_plan = consultar_deepseek([
                    {"role": "system", "content": "Eres un arquitecto de longevidad."},
                    {"role": "user", "content": prompt_plan}
                ])
                st.markdown(res_plan)
                st.session_state.solicitar_plan = False
            except Exception as e:
                st.error(f"Error de conexión: {e}")
