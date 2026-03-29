import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from src.config.settings import EMBEDDING_MODEL, CHROMA_PATH
from src.config.logger import logger


class VectorDB:
    """
    Wrapper para o ChromaDB com integração OllamaEmbeddings.

    Responsabilidades:
        - Gerenciar conexão com o ChromaDB persistente
        - Expor retriever compatível com LangChain
        - Adicionar e buscar documentos vetorizados
        - Garantir integridade dos dados (sem duplicatas)
    """
    def __init__(self):
        """
        Inicializa o ChromaDB com OllamaEmbeddings.
        """
        try:
            # Certifica-se de que o diretório existe
            os.makedirs(CHROMA_PATH, exist_ok=True)

            # Inicializa o embedding model
            self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

            # Inicializa o ChromaDB
            self.db = Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=self.embeddings
            )

            logger.info("ChromaDB inicializado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao inicializar ChromaDB: {e}")
            raise

    def source_exists(self, source_id: str) -> bool:
        """
        Verifica se um source_id já existe no banco.
        Chamada rápida (sem embedding, sem busca vetorial) — usa o filtro
        de metadados direto na collection do Chroma.

        Args:
            source_id: Identificador único da fonte (ex: SHA256 da URL).
        Returns:
            True se já existir pelo menos um documento com esse source_id.
        """
        try:
            results = self.db.get(where= {"source_id": source_id}, limit= 1)
            exists = bool(results and results.get("ids"))
            if exists:
                logger.info(f"source_id '{source_id[:16]}....' já existe no banco.")
            return(exists)
        except Exception as e:
            logger.error(f"Erro ao verificar duplicada para '{source_id[:16]}...': {e}")
            raise

    def add_chunks(self, chunks) -> int:
        """
        Adiciona chunks ao banco de dados vetorial.

        Args:
            chunks: Lista de objetos Document com page_content e metadata.

        Returns:
            Número de chunks adicionados.
        """

        if not chunks:
            logger.warning("add_chunks chamado com lista vazia.")
            return 0

        try:
            self.db.add_documents(chunks)
            logger.info(f"{len(chunks)} chunks adicionados ao ChromaDB.")
            return len(chunks)

        except Exception as e:
            logger.error(f"Erro ao adicionar chunks ao ChromaDB: {e}")
            raise

    def retriever(self, k=5):
        """
        Retorna um retriever LangChain configurado.

        Args:
            k: Número de documentos similares a retornar.
        """
        return self.db.as_retriever(search_kwargs={"k": k})