import uuid

import streamlit as st

from src.ingestion.pipelines import youtube_pipeline
from src.services.chat_engine import ChatAssistant

st.set_page_config(
    page_title="VideoBrain V2",
    page_icon="🧠",
    layout="wide",
)

CATEGORIES = ["Estudos", "Finanças", "Tecnologia", "Saúde", "Outros"]


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
# Abas
# ---------------------------------------------------------------------------
tab1, tab2 = st.tabs(["💬 Chat", "▶️ YouTube"])

# ---------------------------------------------------------------------------
# Aba 1 — Chat (T18)
# ---------------------------------------------------------------------------
with tab1:
    st.header("Chat com o seu Segundo Cérebro")

    # Renderiza histórico de mensagens da sessão
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input do utilizador
    if prompt := st.chat_input("Faça uma pergunta sobre o seu conteúdo..."):
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

# ---------------------------------------------------------------------------
# Aba 2 — Ingestão YouTube (T17)
# ---------------------------------------------------------------------------
with tab2:
    st.header("Ingerir Vídeo do YouTube")

    url = st.text_input(
        "URL do YouTube",
        placeholder="https://www.youtube.com/watch?v=...",
    )
    category = st.selectbox("Categoria", CATEGORIES)

    if st.button("▶️ Ingerir Vídeo", disabled=not url.strip()):
        with st.spinner("A descarregar, transcrever e indexar... (pode demorar alguns minutos)"):
            try:
                n_chunks = youtube_pipeline.run(url=url.strip(), category=category)
                st.success(f"Ingestão concluída! {n_chunks} fragmentos armazenados na base de conhecimento.")
            except ValueError as e:
                st.error(f"Erro na URL ou download: {e}")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")
