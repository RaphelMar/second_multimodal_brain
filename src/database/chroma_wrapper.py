import os
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from src.config.settings import CHROMA_PATH
from src.config.logger import logger


class VectorDB:
    """Wrapper para o ChromaDB com injeção de dependência."""
    def __init__(self, embeddings: Embeddings):
        """
        Inicializa o ChromaDB exigindo o modelo de embeddings por injeção.
        """
        try:
            # Certifica-se de que o diretório existe
            os.makedirs(CHROMA_PATH, exist_ok=True)

            # Inicializa o embedding model
            self._embeddings = embeddings

            # Inicializa o ChromaDB
            self._db = Chroma(
                persist_directory=CHROMA_PATH,
                embedding_function=self._embeddings
            )

            logger.info("ChromaDB inicializado com sucesso via DI.")
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
            results = self._db.get(where= {"source_id": source_id}, limit= 1)
            exists = bool(results and results.get("ids"))
            if exists:
                logger.info(f"source_id '{source_id[:16]}....' já existe no banco.")
            return(exists)
        except Exception:
            logger.exception(f"Erro ao verificar duplicada para '{source_id[:16]}...'")
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
            self._db.add_documents(chunks)
            logger.info(f"{len(chunks)} chunks adicionados ao ChromaDB.")
            return len(chunks)

        except Exception:
            logger.exception(f"Erro ao adicionar chunks ao ChromaDB")
            raise

    def retriever(self, k=5):
        """
        Retorna um retriever LangChain configurado.
        Args:
            k: Número de documentos similares a retornar.
        """
        return self._db.as_retriever(search_kwargs={"k": k})