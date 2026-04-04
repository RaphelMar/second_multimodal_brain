import gc
import os

from faster_whisper import WhisperModel
from src.config.logger import logger


class WhisperTranscriber:
    """
    Transcritor local baseado em faster-whisper.
    Inicializa o modelo sob demanda para controle explícito de memória.
    """
    def __init__(self):
        """
        Inicializa o modelo faster-whisper com as configurações padrão
        para execução local em Apple Silicon (CPU + int8).
        """
        try:
            logger.info(
                f"Carregando modelo Whisper..."
            )
            self.model = WhisperModel(
                model_size_or_path= "large-v3",
                device="cpu",
                compute_type="int8",
            )
            logger.info("Modelo Whisper carregado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo Whisper: {e}")
            raise

    def transcribe(self, audio_path: str) -> str:
        """
        Transcreve o ficheiro de áudio e liberta o modelo da memória imediatamente.

        A regra estrita de memória garante que `self.model` seja destruído e o
        garbage collector seja invocado ANTES de retornar a string, evitando OOM
        durante o processamento subsequente (SemanticChunker + Ollama embeddings).

        Args:
            audio_path (str): Caminho absoluto do ficheiro de áudio a transcrever.

        Returns:
            str: Texto completo da transcrição.

        Raises:
            FileNotFoundError: Se o ficheiro de áudio não existir.
            RuntimeError: Se a transcrição falhar.
        """
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Ficheiro de áudio não encontrado: {audio_path}")

        try:
            logger.info(f"Iniciando transcrição: {audio_path}")
            segments, info = self.model.transcribe(
                audio_path,
                beam_size=8,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
                repetition_penalty=1.15,
                condition_on_previous_text=False
            )

            logger.info(
                f"Idioma detectado: '{info.language}' "
                f"(probabilidade: {info.language_probability:.2f})"
            )

            transcript = " ".join(segment.text.strip() for segment in segments)
            logger.info("Transcrição concluída. Libertando modelo da memória...")

        except Exception as e:
            logger.error(f"Erro durante a transcrição: {e}")
            raise RuntimeError(f"Falha na transcrição de '{audio_path}': {e}") from e

        finally:
            # Regra estrita de memória (BLUEPRINT KPI: Zero OOM)
            # O modelo deve ser destruído antes do SemanticChunker + Ollama serem iniciados.
            del self.model
            gc.collect()
            logger.info("Modelo Whisper removido da memória.")

        return transcript
