import streamlit as st
import google.generativeai as genai
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
        /* Estilo para los mensajes del Coach */
        .stChatMessage { border-radius: 15px; border: 1px solid #1f2937; margin-bottom: 10px; }
        </style>
        """, unsafe_allow_html=True)

style_architect()

# ==========================================
# 2. CONEXIÓN NEURONAL (GEMINI 2.0 FLASH)
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# ==========================================
# 3. BARRA LATERAL - PANEL DE CONTROL
# ==========================================
with st.sidebar:
    # Logo e Identidad
    try:
        st.image("logo_quantum.png", use_container_width=True)
    except:
        st.header("🧬 Quantum Architect")
    
    st.markdown("---")
    st.subheader("🛠️ Parámetros de Diseño")
    
    # Datos que alimentan la inteligencia de la IA
    edad = st.slider("Edad Cronológica:", 18, 100, 45)
    foco = st.selectbox("Área a Optimizar:", 
                        ["Vitalidad Energética", "Claridad Mental", "Longevidad Celular", "Salud Metabólica"])
    
    st.markdown("---")
    if st.button("🗑️ Reiniciar Consultoría", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("🔒 Salir", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

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
            
            # El "System Prompt" que define la filosofía que me diste
            contexto_filosofico = f"""
            Eres el 'Quantum Life Architect', el coach de salud y vida definitivo.
            FILOSOFÍA: La edad es un dato, no un destino. El enemigo es la ignorancia y el abandono.
            PERFIL USUARIO: Edad {edad}, Objetivo principal: {foco}.
            
            DIRECTIVAS DE RESPUESTA:
            1. EDUCAR: Explica la ciencia detrás de su duda (ej. por qué baja la energía).
            2. DESMITIFICAR: Rompe el mito de 'es por la edad'.
            3. ACCIÓN: Da 3 pasos concretos (Bio-hacks, nutrición o ejercicio).
            4. ECOSISTEMA: Indica si necesita profundizar en:
               - Quantum Mind (Psicología/Estrés)
               - Quantum Supplements (Carencias nutricionales)
               - Especialista Médico (Si detectas riesgo real).
            """
            
            try:
                response = model.generate_content([contexto_filosofico, prompt])
                res_text = response.text
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"Error de conexión: {e}")