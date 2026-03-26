import os
import tempfile
import yt_dlp
from src.config.logger import logger

def download_audio(url: str) -> str:
    """
    Faz o download do áudio de uma URL do YouTube para /tmp/ usando yt-dlp.

    Args:
        url (str): URL do vídeo do YouTube.
    Returns:
        str: Caminho absoluto do ficheiro de áudio descarregado.
    Raises:
        ValueError: Se a URL for inválida ou o download falhar.
    """
    if not url or not url.strip():
        raise ValueError("URL não pode ser vazia.")

    output_template = os.path.join(tempfile.gettempdir(), "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        logger.info(f"Iniciando download de áudio: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info.get("id", "")
            audio_path = os.path.join(tempfile.gettempdir(), f"{video_id}.mp3")

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Ficheiro de áudio não encontrado após download: {audio_path}")

        logger.info(f"Download concluído: {audio_path}")
        return audio_path

    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Erro no download do YouTube: {e}")
        raise ValueError(f"Falha ao descarregar áudio da URL '{url}': {e}") from e
    except Exception as e:
        logger.error(f"Erro inesperado no youtube_extractor: {e}")
        raise
