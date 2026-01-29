import streamlit as st
import requests
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
# 2. CONEXIÓN NEURONAL (DEEPSEEK API)
# ==========================================
DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

def deepseek_chat(messages):
    """Envía mensajes al modelo DeepSeek y devuelve el texto."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(DEEPSEEK_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"DeepSeek Error: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]

# ==========================================
# 3. BARRA LATERAL - PANEL DE CONTROL
# ==========================================
with st.sidebar:
    try:
        st.image("logo_quantum.png", use_container_width=True)
    except:
        st.header("🧬 Quantum Architect")
    
    st.markdown("---")
    st.subheader("🛠️ Parámetros de Diseño")
    
    edad = st.slider("Edad Cronológica:", 18, 100, 45)
    st.markdown("---")

    genero = st.radio("Género Biológico:", ["Masculino", "Femenino"], horizontal=True)
    
    st.markdown("---")
    st.subheader("📋 Estado de Vitalidad Actual")
    
    insomnio = st.checkbox("Dificultad para dormir")
    energia = st.checkbox("Fatiga por la tarde")
    articulaciones = st.checkbox("Molestias articulares")
    estres = st.checkbox("Nivel de estrés alto")
    
    lista_sintomas = []
    if insomnio: lista_sintomas.append("Insomnio")
    if energia: lista_sintomas.append("Baja energía vespertina")
    if articulaciones: lista_sintomas.append("Dolores articulares")
    if estres: lista_sintomas.append("Estrés crónico")
    
    st.session_state.sintomas_reportados = lista_sintomas

    foco = st.selectbox("Área a Optimizar:", 
                        ["Vitalidad Energética", "Claridad Mental", "Longevidad Celular", "Salud Metabólica"])
    
    st.markdown("---")
    if st.button("🗑️ Reiniciar Consultoría", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    if st.button("📝 Generar Plan Maestro", use_container_width=True):
        if st.session_state.messages:
            st.session_state.solicitar_plan = True
        else:
            st.warning("Primero describe tu situación en el chat.")

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

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# 5. CEREBRO DEL ARCHITECT (DeepSeek)
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

DIRECTIVAS:
- Usa la biología de su género ({genero}) para dar consejos precisos.
- Desmitifica que sus síntomas sean “normales por la edad”.
- Propón 3 acciones de arquitectura de vida.
- Sugiere Quantum Mind o Supplements si el caso lo requiere.
"""

            try:
                respuesta = deepseek_chat([
                    {"role": "system", "content": contexto_filosofico},
                    {"role": "user", "content": prompt}
                ])
                st.markdown(respuesta)
                st.session_state.messages.append({"role": "assistant", "content": respuesta})

            except Exception as e:
                st.error(f"Error de conexión con DeepSeek: {e}")

    # ==========================================
    # 6. GENERADOR DEL PLAN MAESTRO
    # ==========================================
    if st.session_state.get("solicitar_plan"):
        with st.chat_message("assistant", avatar="🏛️"):
            with st.spinner("Diseñando tu Plan Maestro de Longevidad..."):

                historial = str(st.session_state.messages)

                prompt_plan = f"""
Basado en nuestra consultoría: {historial}.
Genera un 'Plan Maestro de Longevidad Quantum' con:
1. Diagnóstico de Hábitos Actuales.
2. Protocolo de Acción (Mañana, Tarde, Noche).
3. Sugerencia de Expertos.
Tono: Arquitecto Jefe, directo y visionario.
"""

                try:
                    plan = deepseek_chat([
                        {"role": "system", "content": "Eres un Arquitecto de Longevidad de élite."},
                        {"role": "user", "content": prompt_plan}
                    ])
                    st.markdown(plan)

                except Exception as e:
                    st.error(f"Error generando el plan maestro: {e}")

                st.session_state.solicitar_plan = False
