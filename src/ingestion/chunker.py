import hashlib
from typing import Any
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from src.config.logger import logger
from src.config.settings import (
    CHUNKER_BREAKPOINT_THRESHOLD,
    CHUNKER_MIN_CHUNK_CHARS,
    CHUNKER_MAX_CHUNK_CHARS,
    FALLBACK_OVERLAP
)


class SemanticProcessor:
    """Processador semântico para divisão de texto usando DI."""

    def __init__(self, embeddings: Embeddings):
        """
        Inicializa o SemanticChunker com embeddings do Ollama.
        """
        self.embeddings = embeddings
        self.semantic_chunker = SemanticChunker(
            self.embeddings,
            breakpoint_threshold_type= "percentile",
            breakpoint_threshold_amount= CHUNKER_BREAKPOINT_THRESHOLD
        )

        self.fallback_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNKER_MAX_CHUNK_CHARS,
            chunk_overlap=FALLBACK_OVERLAP,
            separators=["\n\n", "\n", ". ", "? ", "! ", " ", ""]
        )

    def _generate_source_id(self, content: str) -> str:
        """
        Gera um ID único baseado no conteúdo usando SHA-256.
        Args:
            content (str): Conteúdo para gerar o hash.
        Returns:
            str: Hash SHA-256 do conteúdo.
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def process_and_format(self, text: str, metadata_dict: dict[str, Any]) -> list[Document]:
        """
        Processa o texto usando SemanticChunker e formata os metadados.
        Args:
            text (str): Texto a ser dividido em chunks.
            metadata_dict (dict): Dicionário com metadados (source_type, category, title).
        Returns:
            list[Document]: Lista de objetos Document com conteúdo e metadados formatados.
        """
        try:
            # Guard Clause: Aborta processamento se o texto for vazio/nulo
            if not text or not text.strip():
                logger.warning(
                    "Texto vazio recebido. Abortando processamento.", 
                    extra={"source_id": metadata_dict.get("source_id")}
                )
                return []
            
            # Divide o texto em chunks semanticamente
            raw_chunks = self.semantic_chunker.split_text(text)

            chunks: list[str] = []
            giant_chunks = 0

            for chunk in raw_chunks:
                tamanho = len(chunk)
                if tamanho < CHUNKER_MIN_CHUNK_CHARS:
                    continue
                
                if tamanho > CHUNKER_MAX_CHUNK_CHARS:
                    giant_chunks += 1
                    chunks.extend(self.fallback_splitter.split_text(chunk))

                else:
                    chunks.append(chunk)

            # Prepara os metadados base
            base_metadata = {
                "source_type": metadata_dict.get("source_type", "unknown"),
                "category": metadata_dict.get("category", "general"),
                "title": metadata_dict.get("title", "untitled")
            }

            # Usa source_id do metadata_dict (hash da URL/path do pipeline)
            # ou gera a partir do texto como fallback
            base_metadata["source_id"] = metadata_dict.get("source_id") or self._generate_source_id(text)

            # Cria lista de Documentos com metadados
            documents = [
                Document(
                    page_content=chunk,
                    metadata={**base_metadata, "chunk_index": i}
                )
                for i, chunk in enumerate(chunks)
            ]

            logger.info("processamento_concluido", extra={
                "total_chunks": len(documents),
                "fallbacks_acionados": giant_chunks
            })
            return documents

        except Exception:
            logger.exception("Erro crítico ao processar texto.")
            raise