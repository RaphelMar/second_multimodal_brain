import uuid
import streamlit as st

from src.services.chat_engine import ChatAssistant

st.set_page_config(
    page_title="Samantha Eve Wilkins",
    page_icon="👩🏻‍💻",
    layout="wide",
)

@st.cache_resource
def get_assistant() -> ChatAssistant:
    """Instancia o ChatAssistant uma única vez por sessão do servidor."""
    return ChatAssistant()

# Garante um session_id único e persistente por aba do browser
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# Área Principal — Chat
# ---------------------------------------------------------------------------
st.header("Samantha Eve Wilkins")

# Renderiza histórico de mensagens da sessão
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input do utilizador (livre no fluxo principal para o auto-scroll funcionar nativamente)
if prompt := st.chat_input("Digite uma mensagem"):
    # Exibe a mensagem do utilizador imediatamente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Gera e exibe a resposta em streaming
    with st.chat_message("assistant"):
        assistant = get_assistant()
        response = st.write_stream(
            assistant.get_response(prompt, session_id=st.session_state.session_id)
        )

    st.session_state.messages.append({"role": "assistant", "content": response})