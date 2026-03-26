import hashlib
import os

import yt_dlp

from src.ingestion.extractors.youtube_extractor import download_audio
from src.ingestion.transcribers.local_whisper import WhisperTranscriber
from src.ingestion.chunker import SemanticProcessor
from src.database.chroma_wrapper import VectorDB
from src.config.logger import logger


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
        1. Extrai título via yt-dlp (sem download)
        2. Faz download do áudio para /tmp/
        3. Transcreve com faster-whisper (modelo destruído ao final)
        4. Apaga o ficheiro de áudio
        5. Processa o texto com SemanticChunker
        6. Persiste os chunks no ChromaDB

    Args:
        url (str): URL do vídeo do YouTube.
        category (str): Categoria definida pelo utilizador na UI.

    Returns:
        int: Número de chunks armazenados no ChromaDB.
    """
    logger.info(f"[youtube_pipeline] Iniciando pipeline para: {url}")

    # 1. Título
    title = _extract_title(url)
    logger.info(f"[youtube_pipeline] Título: {title}")

    # 2. Download do áudio
    audio_path = download_audio(url)

    # 3. Transcrição — o modelo Whisper é destruído dentro de transcribe()
    transcriber = WhisperTranscriber()
    transcript = transcriber.transcribe(audio_path)

    # 4. Apagar ficheiro de áudio (liberta disco imediatamente)
    try:
        os.remove(audio_path)
        logger.info(f"[youtube_pipeline] Ficheiro de áudio removido: {audio_path}")
    except OSError as e:
        logger.warning(f"[youtube_pipeline] Não foi possível remover o áudio: {e}")

    # 5. Chunking semântico
    source_id = hashlib.sha256(url.encode("utf-8")).hexdigest()
    processor = SemanticProcessor()
    chunks = processor.process_and_format(
        text=transcript,
        metadata_dict={
            "source_id": source_id,
            "source_type": "youtube",
            "category": category,
            "title": title,
        },
    )

    # 6. Persistência no ChromaDB
    db = VectorDB()
    db.add_chunks(chunks)

    logger.info(f"[youtube_pipeline] Pipeline concluído. {len(chunks)} chunks armazenados.")
    return len(chunks)
