import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do modelo LLM
LLM_MODEL = os.getenv("LLM_MODEL", "gemma3n:e4b")

# Configurações do modelo de embedding
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embeddinggemma:300m")

# Configurações dos chuncks
CHUNKER_BREAKPOINT_THRESHOLD = os.getenv("CHUNKER_BREAKPOINT_THRESHOLD", 90)
CHUNKER_MIN_CHUNK_CHARS = os.getenv("CHUNKER_BREAKPOINT_THRESHOLD", 100)

# Caminho para o banco de dados ChromaDB
CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chromadb")

# Prompt de sistema do assistente (injetável via .env para troca de persona)
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
