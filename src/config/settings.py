import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações LLMs
LLM_MODEL_LOCAL = os.getenv("LLM_MODEL_LOCAL")
LLM_MODEL_CLAUD = os.getenv("LLM_MODEL_CLAUD")

# Configurações para o banco vetoria
CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chromadb")

# Configurações da Semantantica
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embeddinggemma:300m")
CHUNKER_BREAKPOINT_THRESHOLD = float(os.getenv("CHUNKER_BREAKPOINT_THRESHOLD", 90))
CHUNKER_MIN_CHUNK_CHARS = int(os.getenv("CHUNKER_MIN_CHUNK_CHARS", 100))
CHUNKER_MAX_CHUNK_CHARS = int(os.getenv("CHUNKER_MAX_CHUNK_CHARS", 1000))
FALLBACK_OVERLAP = int(os.getenv("FALBACK_OVERLAP", 250))
RETRIEVER_K = os.getenv("RETRIEVER_K", 5)
RETRIEVER_THRESHOLD = os.getenv("RETRIEVER_THRESHOLD", 5)


# Configuracoes System Prompt
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
CONTEXTUALIZE = os.getenv("CONTEXTUALIZE")
