import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do modelo LLM
LLM_MODEL = os.getenv("LLM_MODEL", "gemma3n:e4b")

# Configurações do modelo de embedding
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embeddinggemma:300m")

# Caminho para o banco de dados ChromaDB
CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chromadb")

# Prompt de sistema do assistente (injetável via .env para troca de persona)
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "Você é um assistente inteligente de segundo cérebro. "
    "Responda com base no contexto fornecido. "
    "Se a informação não estiver no contexto, diga que não sabe.",
)