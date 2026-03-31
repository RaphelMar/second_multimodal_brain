import hashlib
import os
import gc

import yt_dlp
from langchain_ollama import OllamaEmbeddings

from src.ingestion.extractors.youtube_extractor import download_audio
from src.ingestion.transcribers.local_whisper import WhisperTranscriber
from src.ingestion.chunker import SemanticProcessor
from src.database.chroma_wrapper import VectorDB
from src.config.logger import logger
from src.config.settings import EMBEDDING_MODEL


def _extract_title(url: str) -> str:
    """Extrai o título do vídeo sem fazer download."""
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("title", url)
    except Exception:
        return url

def run(url: str, category: str) -> int:
    """
    Orquestra o pipeline completo de ingestão de vídeo do YouTube.

    Fluxo:
        1. Gera source_id e verifica duplicata (antes de qualquer trabalho pesado)
        2. Extrai título via yt-dlp (sem download)
        3. Faz download do áudio para /tmp/
        4. Transcreve com faster-whisper (modelo destruído ao final)
        5. Apaga o ficheiro de áudio
        6. Processa o texto com SemanticChunker
        7. Persiste os chunks no ChromaDB

    Args:
        url: URL do vídeo do YouTube.
        category: Categoria definida pelo utilizador na UI.

    Returns:
        Número de chunks armazenados no ChromaDB (0 se duplicata).
    """
    logger.info(f"[youtube_pipeline] Iniciando pipeline para: {url}")

    # 1. Instancia o Embedding centralizado (Single Source of Truth)
    embeddings_model = OllamaEmbeddings(model=EMBEDDING_MODEL)

    # 2. Injeta dependência no banco e verifica duplicata
    db = VectorDB(embeddings=embeddings_model)
    source_id = hashlib.sha256(url.encode("utf-8")).hexdigest()

    if db.source_exists(source_id):
        logger.info(f"[youtube_pipeline] Vídeo já processado. Pulando: {url}")
        return 0

    # 3. Título
    title = _extract_title(url)
    logger.info(f"[youtube_pipeline] Título: {title}")

    # 4. Download do áudio
    audio_path = download_audio(url)

    # 5. Transcrição — o modelo Whisper é destruído dentro de transcribe()
    transcriber = WhisperTranscriber()
    transcript = transcriber.transcribe(audio_path)

    # 6 Limpeza critica de memoria
    del transcriber
    gc.collect()

    # 7. Apagar ficheiro de áudio (liberta disco imediatamente)
    try:
        os.remove(audio_path)
        logger.info(f"[youtube_pipeline] Ficheiro de áudio removido: {audio_path}")
    except OSError as e:
        logger.warning(f"[youtube_pipeline] Não foi possível remover o áudio: {e}")

    # 8. Chunking semântico
    processor = SemanticProcessor(embeddings=embeddings_model)
    chunks = processor.process_and_format(
        text=transcript,
        metadata_dict={
            "source_id": source_id,
            "source_type": "youtube",
            "category": category,
            "title": title,
        },
    )

    # 9. Persistência no ChromaDB
    added = db.add_chunks(chunks)
    logger.info(f"[youtube_pipeline] Pipeline concluído. {added} chunks armazenados.")
    return len(chunks)
