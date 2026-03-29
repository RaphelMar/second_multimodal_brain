from typing import Generator

from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

from src.config.settings import LLM_MODEL, SYSTEM_PROMPT
from src.config.logger import logger
from src.database.chroma_wrapper import VectorDB


class ChatAssistant:
    """
    Motor de chat RAG com histórico de sessão em memória.

    A persona é controlada inteiramente por SYSTEM_PROMPT (settings.py / .env),
    garantindo o critério de agnosticismo de agente do BLUEPRINT.
    """

    def __init__(self):
        """
        Instancia o ChatOllama, o retriever do ChromaDB e monta a cadeia RAG
        com suporte a histórico de conversação por sessão.
        """
        try:
            logger.info(f"Inicializando ChatAssistant com modelo '{LLM_MODEL}'...")

            self.llm = ChatOllama(model=LLM_MODEL, temperature=0.5)
            self._sessions: dict[str, InMemoryChatMessageHistory] = {}

            vector_db = VectorDB()
            retriever = vector_db.retriever(k= 5)

            self._chain = self._build_chain(retriever)
            logger.info("ChatAssistant inicializado com sucesso.")

        except Exception as e:
            logger.error(f"Erro ao inicializar ChatAssistant: {e}")
            raise

    def _build_chain(self, retriever) -> RunnableWithMessageHistory:
        """
        Constrói a cadeia RAG completa:
          1. History-aware retriever — reformula a query com base no histórico.
          2. Stuff documents chain — responde usando o contexto recuperado.
          3. Retrieval chain — combina os dois anteriores.
          4. RunnableWithMessageHistory — injeta o histórico por session_id.
        """
        # Prompt para reformular a pergunta como query independente do histórico
        contextualize_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Dado o histórico de chat e a última pergunta do utilizador, "
                "reformule a pergunta como uma query independente e autocontida, "
                "sem alterar o seu significado. Se já for independente, retorne-a sem modificações.",
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        history_aware_retriever = create_history_aware_retriever(
            self.llm, retriever, contextualize_prompt
        )

        # Prompt principal de QA com contexto vetorial
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT + "\n\nContexto relevante:\n{context}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        qa_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

        return RunnableWithMessageHistory(
            rag_chain,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def _get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        """Devolve (ou cria) o histórico em memória para a sessão dada."""
        if session_id not in self._sessions:
            self._sessions[session_id] = InMemoryChatMessageHistory()
        return self._sessions[session_id]

    def get_response(self, question: str, session_id: str = "default") -> Generator[str, None, None]:
        """
        Gera a resposta em modo streaming, compatível com `st.write_stream`.

        Args:
            question (str): Pergunta do utilizador.
            session_id (str): Identificador da sessão (mantém histórico isolado por utilizador).

        Yields:
            str: Fragmentos de texto da resposta à medida que são gerados pelo LLM.
        """
        logger.info(f"[ChatAssistant] Nova pergunta (sessão '{session_id}'): {question[:80]}...")

        for chunk in self._chain.stream(
            {"input": question},
            config={"configurable": {"session_id": session_id}},
        ):
            if answer_chunk := chunk.get("answer", ""):
                yield answer_chunk
