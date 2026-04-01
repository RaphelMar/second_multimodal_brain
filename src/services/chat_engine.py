import os
from typing import Generator

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch

from langchain_ollama import ChatOllama, OllamaEmbeddings

# Importamos o EMBEDDING_MODEL para injetar a dependência no banco
from src.config.logger import logger
from src.database.chroma_wrapper import VectorDB
from src.config.settings import (
    LLM_MODEL_LOCAL,
    LLM_MODEL_CLAUD,
    EMBEDDING_MODEL,
    SYSTEM_PROMPT,
    CONTEXTUALIZE,
    RETRIEVER_K,
    RETRIEVER_THRESHOLD
)

class ChatAssistant:
    """
    Motor de chat RAG com histórico de sessão em memória,
    construído puramente com LCEL (LangChain Expression Language).
    """

    def __init__(self):
        try:
            logger.info(f"Inicializando ChatAssistant...")

            llm_local = ChatOllama(model=LLM_MODEL_LOCAL, temperature=0.5, num_ctx=16384)
            llm_claud = ChatOllama(model=LLM_MODEL_CLAUD, temperature=0.5, num_ctx=16384)

            self.llm = llm_claud.with_fallbacks([llm_local])
            self._sessions: dict[str, InMemoryChatMessageHistory] = {}

            embedding_model = OllamaEmbeddings(model=EMBEDDING_MODEL)
            vector_db = VectorDB(embeddings= embedding_model)
            retriever = vector_db.retriever(k= RETRIEVER_K, score_threshold= RETRIEVER_THRESHOLD)

            self._chain = self._build_chain(retriever)
            logger.info("ChatAssistant inicializado com sucesso.")

        except Exception:
            logger.exception("Erro ao inicializar ChatAssistant")
            raise

    def _load_system_prompt(self, system_prompt: str) -> str:
        """
        Lê o prompt do sistema a partir do ficheiro .md referenciado no .env.
        Inclui um fallback de segurança caso o ficheiro seja movido ou apagado.
        """
        fallback = "Você é um assistente de IA focado em ajudar o utilizador."
        if not system_prompt:
            return fallback
        
        try:
            with open(system_prompt, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception: 
            logger.exception(f"Erro ao ler o ficheiro de prompt '{system_prompt}'. Usando fallback.")
            return fallback

    def _format_docs(self, docs) -> str:
        """Utilitário LCEL: Converte os chunks vetoriais numa única string."""
        return "\n\n".join(doc.page_content for doc in docs)

    def _build_chain(self, retriever) -> RunnableWithMessageHistory:
        """
        Orquestra a cadeia RAG usando a sintaxe declarativa LCEL (|).
        """
        # 1. Reformulação da Pergunta (History-Aware)
        contextualize_content = self._load_system_prompt(system_prompt= CONTEXTUALIZE)
        contextualize_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_content),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        condense_question_chain = contextualize_prompt | self.llm | StrOutputParser()
        history_aware_retriever = RunnableBranch(
            (lambda x: bool(x.get("chat_history")), condense_question_chain | retriever),
            (lambda x: x["input"]) | retriever 
        )

        # 2. Prompt principal de QA com contexto vetorial
        system_prompt_content = self._load_system_prompt(system_prompt= SYSTEM_PROMPT)
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_content + "\n<rag_context>\n{context}\n</rag_context>"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        # 3. O coração do LCEL: O Pipeline Declarativo
        # Lê-se: Atribui o contexto -> Passa para o prompt -> Executa LLM -> Converte para String
        rag_chain = (
            RunnablePassthrough.assign(context= history_aware_retriever | self._format_docs)
            | qa_prompt
            | self.llm
            | StrOutputParser()
        )
    
        return RunnableWithMessageHistory(
            rag_chain,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history"
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
            yield chunk
