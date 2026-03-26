import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from src.config.settings import EMBEDDING_MODEL, CHROMA_PATH
from src.config.logger import logger


class VectorDB:
    """
    Wrapper para o ChromaDB com integração OllamaEmbeddings.
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

    def add_chunks(self, chunks):
        """
        Adiciona chunks ao banco de dados vetorial.
        Args:
            chunks (list): Lista de objetos Document com page_content e metadata.
        """
        try:
            self.db.add_documents(chunks)
            logger.info(f"{len(chunks)} chunks adicionados ao ChromaDB.")
        except Exception as e:
            logger.error(f"Erro ao adicionar chunks ao ChromaDB: {e}")
            raise

    def search(self, query, k=5):
        """
        Realiza uma busca vetorial no banco de dados.
        Args:
            query (str): Texto da consulta.
            k (int): Número de resultados desejados. Padrão é 5.
        Returns:
            list: Lista de documentos similares.
        """
        try:
            results = self.db.similarity_search(query, k=k)
            logger.info(f"Busca realizada com sucesso. {len(results)} resultados encontrados.")
            return results
        except Exception as e:
            logger.error(f"Erro ao realizar busca no ChromaDB: {e}")
            raise