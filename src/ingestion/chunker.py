import hashlib
from typing import List, Dict, Any
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from src.config.settings import EMBEDDING_MODEL
from src.config.logger import logger


class SemanticProcessor:
    """
    Processador semântico para divisão de texto e formatação de metadados.
    """
    def __init__(self):
        """
        Inicializa o SemanticChunker com embeddings do Ollama.
        """
        try:
            self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
            self.chunker = SemanticChunker(self.embeddings, breakpoint_threshold_type= "percentile", breakpoint_threshold_amount= 90)
            logger.info("SemanticProcessor inicializado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao inicializar SemanticProcessor: {e}")
            raise

    def _generate_source_id(self, content: str) -> str:
        """
        Gera um ID único baseado no conteúdo usando SHA-256.
        Args:
            content (str): Conteúdo para gerar o hash.
        Returns:
            str: Hash SHA-256 do conteúdo.
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def process_and_format(self, text: str, metadata_dict: Dict[str, Any]) -> List[Document]:
        """
        Processa o texto usando SemanticChunker e formata os metadados.
        Args:
            text (str): Texto a ser dividido em chunks.
            metadata_dict (dict): Dicionário com metadados (source_type, category, title).
        Returns:
            List[Document]: Lista de objetos Document com conteúdo e metadados formatados.
        """
        try:
            # Divide o texto em chunks semanticamente
            chunks = self.chunker.split_text(text)

            # Prepara os metadados base
            base_metadata = {
                "source_type": metadata_dict.get("source_type", "unknown"),
                "category": metadata_dict.get("category", "general"),
                "title": metadata_dict.get("title", "untitled")
            }

            # Usa source_id do metadata_dict (hash da URL/path do pipeline)
            # ou gera a partir do texto como fallback
            base_metadata["source_id"] = metadata_dict.get(
                "source_id", self._generate_source_id(text)
            )

            # Cria lista de Documentos com metadados
            documents = []
            for i, chunk in enumerate(chunks):
                # Adiciona índice do chunk aos metadados
                chunk_metadata = base_metadata.copy()
                chunk_metadata["chunk_index"] = i

                doc = Document(
                    page_content=chunk,
                    metadata=chunk_metadata
                )
                documents.append(doc)

            logger.info(f"Texto processado em {len(documents)} chunks.")
            return documents

        except Exception as e:
            logger.error(f"Erro ao processar texto: {e}")
            raise