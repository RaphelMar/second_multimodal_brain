# Resumo da Implementação - Tarefa T01

## Tarefa Executada
**T01:** Criar estrutura de pastas (`src/config`, `src/database`, `src/ingestion`, `src/services`, `data/chromadb`).

## Descrição Técnica
Foi criada a estrutura de pastas do projeto conforme especificado no blueprint. As seguintes operações foram realizadas:

1. Criação da hierarquia de diretórios principais:
   - Pasta raiz `src` para código-fonte
   - Pasta raiz `data` para armazenamento de dados

2. Dentro da pasta `src`, foram criados os seguintes diretórios:
   - `config`: Para configurações globais do projeto
   - `database`: Para wrappers e interfaces do banco de dados
   - `ingestion`: Para módulos de ingestão de diferentes tipos de conteúdo
   - `services`: Para motores de serviço como o chat RAG

3. Dentro da pasta `data`, foi criado o diretório:
   - `chromadb`: Para persistência local do banco vetorial

## Comandos Utilizados
```bash
mkdir -p src/config src/database src/ingestion src/services data/chromadb
```

## Estrutura Resultante
```
.
├── data/
│   └── chromadb/
└── src/
    ├── config/
    ├── database/
    ├── ingestion/
    └── services/
```

A estrutura de pastas foi criada com sucesso, estabelecendo a fundação para o desenvolvimento do projeto VideoBrain V2.

# Resumo da Implementação - Tarefa T02

## Tarefa Executada
**T02:** Criar o ficheiro `requirements.txt` com todas as dependências do projeto e instalar no ambiente virtual.

## Descrição Técnica
Foi criado o arquivo `requirements.txt` contendo todas as dependências necessárias para o projeto, com suas respectivas versões fixadas para garantir a estabilidade e reprodutibilidade do ambiente de desenvolvimento. As dependências incluem tanto bibliotecas para a interface web quanto para processamento de dados, transcrição de áudio, extração de documentos e funcionalidades de busca vetorial.

## Dependências Adicionadas
- streamlit: Framework para criação da interface web
- langchain e extensões: Core do sistema RAG e integração com ChromaDB e Ollama
- faster-whisper: Biblioteca para transcrição local de áudio
- yt-dlp: Ferramenta para download de vídeos do YouTube
- docling: Biblioteca para extração de texto de documentos complexos
- python-dotenv: Gerenciamento de variáveis de ambiente

## Conteúdo do Arquivo
```
streamlit==1.39.0
langchain==0.3.7
langchain-ollama==0.2.0
langchain-chroma==0.1.4
langchain-experimental==0.3.2
faster-whisper==1.0.3
yt-dlp==2024.11.18
docling==2.3.2
python-dotenv==1.0.1
```

# Resumo da Implementação - Tarefa T03

## Tarefa Executada
**T03:** Criar ficheiro `.env` com as configurações (ex: `LLM_MODEL="gemma3n:e4b"`, `EMBEDDING_MODEL="embeddinggemma:300m"`, `CHROMA_PATH="data/chromadb"`).

## Descrição Técnica
Foi criado o arquivo `.env` na raiz do projeto para armazenar as variáveis de ambiente necessárias para a configuração do sistema. Este arquivo contém as configurações essenciais para os modelos LLM e de embedding, além do caminho para o banco de dados vetorial ChromaDB.

## Variáveis de Ambiente Configuradas
- `LLM_MODEL`: Define o modelo de linguagem a ser utilizado (`gemma3n:e4b`)
- `EMBEDDING_MODEL`: Define o modelo de embedding para vetorização dos textos (`embeddinggemma:300m`)
- `CHROMA_PATH`: Define o caminho onde os dados do ChromaDB serão persistidos (`data/chromadb`)

## Conteúdo do Arquivo
```
LLM_MODEL=gemma3n:e4b
EMBEDDING_MODEL=embeddinggemma:300m
CHROMA_PATH=data/chromadb
```

Este arquivo permite uma fácil configuração e modificação das variáveis do sistema sem a necessidade de alterar o código-fonte.

# Resumo da Implementação - Tarefa T04

## Tarefa Executada
**T04:** Criar `src/config/settings.py` para carregar as variáveis de ambiente utilizando a biblioteca `os` ou `pydantic-settings`.

## Descrição Técnica
Foi criado o arquivo `src/config/settings.py` responsável por carregar as variáveis de ambiente definidas no arquivo `.env`. O arquivo utiliza a biblioteca `python-dotenv` para carregar automaticamente as variáveis do arquivo `.env` e as disponibiliza como constantes no módulo.

## Implementação Realizada
- Importação da biblioteca `os` para acesso às variáveis de ambiente
- Importação da função `load_dotenv` da biblioteca `dotenv` para carregar automaticamente as variáveis do arquivo `.env`
- Definição das constantes `LLM_MODEL`, `EMBEDDING_MODEL` e `CHROMA_PATH` com valores padrão caso as variáveis de ambiente não estejam definidas
- Configuração para carregar automaticamente as variáveis de ambiente ao importar o módulo

## Código Criado
```python
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
```

Esta implementação permite que o sistema utilize configurações personalizadas através do arquivo `.env`, facilitando a manutenção e a portabilidade do projeto.

# Resumo da Implementação - Tarefa T05

## Tarefa Executada
**T05:** Criar `src/config/logger.py` para estabelecer um padrão de registos (logs) no terminal (INFO, DEBUG, ERROR).

## Descrição Técnica
Foi criado o arquivo `src/config/logger.py` responsável por configurar um logger padronizado para o projeto. Este logger permite registrar informações, avisos e erros durante a execução do sistema, facilitando a depuração e monitoramento.

## Implementação Realizada
- Importação das bibliotecas `logging` e `sys` para configuração do logger
- Criação da função `setup_logger` que configura e retorna um logger padronizado
- Definição de um handler que imprime os logs no console (stdout)
- Configuração de um formato padronizado para as mensagens de log
- Criação de uma instância padrão do logger chamada `logger`

## Código Criado
```python
import logging
import sys

def setup_logger(name='video_brain', level=logging.INFO):
    """
    Configura e retorna um logger padronizado para o projeto.

    Args:
        name (str): Nome do logger. Padrão é 'video_brain'.
        level (int): Nível de log. Padrão é logging.INFO.

    Returns:
        logging.Logger: Logger configurado.
    """
    # Cria o logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evita a duplicação de handlers se o logger já existir
    if not logger.handlers:
        # Cria um handler que imprime no console
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Cria um formato para os logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        # Adiciona o handler ao logger
        logger.addHandler(handler)

    return logger

# Cria uma instância padrão do logger
logger = setup_logger()
```

Esta implementação permite que o sistema utilize um logger padronizado para registrar eventos importantes durante a execução, facilitando a identificação e resolução de problemas.

# Resumo da Implementação - Tarefa T06

## Tarefa Executada
**T06:** Criar `src/database/chroma_wrapper.py`. Instanciar a classe `VectorDB` com inicialização do ChromaDB acoplado ao `OllamaEmbeddings`.

## Descrição Técnica
Foi criado o arquivo `src/database/chroma_wrapper.py` contendo a classe `VectorDB` que serve como wrapper para o ChromaDB com integração ao OllamaEmbeddings. Esta classe é responsável por inicializar o banco de dados vetorial, adicionar chunks de texto e realizar buscas vetoriais.

## Implementação Realizada
- Criação da classe `VectorDB` no arquivo `src/database/chroma_wrapper.py`
- Implementação do método `__init__` para inicializar o ChromaDB com OllamaEmbeddings usando as configurações do arquivo `.env`
- Utilização do logger padronizado para registro de eventos
- Tratamento de exceções para garantir robustez nas operações

## Código Criado
```python
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
```

Esta implementação estabelece a base para o armazenamento e recuperação de embeddings vetoriais no projeto VideoBrain V2, permitindo futuras funcionalidades de busca semântica sobre o conteúdo ingerido.

# Resumo da Implementação - Tarefa T08

## Tarefa Executada
**T08:** Criar `src/ingestion/chunker.py`. Implementar a classe `SemanticProcessor` configurando o `SemanticChunker` da LangChain.

## Descrição Técnica
Foi criado o arquivo `src/ingestion/chunker.py` contendo a classe `SemanticProcessor` que utiliza o `SemanticChunker` da LangChain para dividir textos de forma semântica. Esta classe é responsável por processar o conteúdo textual e formatar os metadados necessários para armazenamento no ChromaDB.

## Implementação Realizada
- Criação da classe `SemanticProcessor` no arquivo `src/ingestion/chunker.py`
- Implementação do método `__init__` para inicializar o `SemanticChunker` com embeddings do Ollama
- Criação do método auxiliar `_generate_source_id` para gerar identificadores únicos baseados em SHA-256
- Implementação do método `process_and_format` que:
  - Divide o texto em chunks semanticamente usando `SemanticChunker`
  - Formata os metadados com `source_type`, `category`, `title` e `source_id`
  - Adiciona índice de chunk aos metadados
  - Retorna lista de objetos `Document` prontos para armazenamento

## Código Criado
```python
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
            self.chunker = SemanticChunker(self.embeddings)
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

            # Gera source_id baseado no texto completo
            base_metadata["source_id"] = self._generate_source_id(text)

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
```

Esta implementação permite que o sistema divida o conteúdo ingerido de forma semanticamente coerente, preparando-o para armazenamento vetorial e futuras consultas através do mecanismo de RAG.

# Revisão Técnica e Tarefa T09

## Revisão Geral (Engenheiro Sênior)

### T07 — Marcação Retroativa
Os métodos `add_chunks(chunks)` e `search(query, k=5)` já haviam sido implementados em `src/database/chroma_wrapper.py` durante a execução de T06/T08, mas T07 estava erroneamente marcado como `[ ]` no BLUEPRINT. A marcação foi corrigida para `[x]`.

### Bug Corrigido em `chunker.py`
Foi identificado um desvio em relação à especificação: o `source_id` estava sendo gerado a partir do hash do *conteúdo do texto transcrito*, enquanto o BLUEPRINT define que o `source_id` deve ser o "Hash SHA-256 do arquivo ou URL". Isso causaria colisões caso dois pipelines diferentes gerassem transcrições idênticas, e impediria a deduplicação baseada na fonte original.

**Correção aplicada:** O método `process_and_format` agora prioriza o `source_id` fornecido pelo pipeline via `metadata_dict`. O hash do texto é usado apenas como fallback, garantindo que o pipeline de YouTube (por exemplo) passe `source_id=SHA256(url)`.

---

## Tarefa Executada — T09

**T09:** No `SemanticProcessor`, implementar o método `process_and_format(text, metadata_dict)` que fatia o texto e injeta `source_id`, `source_type`, `category` e `title` em cada fragmento.

O método já existia como parte do trabalho adiantado na T08. A T09 foi formalizada com a correção do comportamento do `source_id`.

## Linha Alterada em `src/ingestion/chunker.py`

```python
# ANTES (gerava source_id a partir do texto — incorreto)
base_metadata["source_id"] = self._generate_source_id(text)

# DEPOIS (respeita source_id do pipeline, fallback para hash do texto)
base_metadata["source_id"] = metadata_dict.get(
    "source_id", self._generate_source_id(text)
)
```

## Contrato do Método `process_and_format`

- **Entrada:** `text` (transcrição ou conteúdo extraído) + `metadata_dict` com chaves: `source_id` (hash da URL/path), `source_type`, `category`, `title`
- **Saída:** `List[Document]` — cada item com `page_content` (chunk semântico) e `metadata` contendo os 4 campos obrigatórios + `chunk_index`
- **Dependência:** O pipeline chamador é responsável por calcular `source_id = SHA256(url_ou_path)` e passá-lo no `metadata_dict`
# Resumo da Implementação - Tarefa T10

## Tarefa Executada
**T10:** Criar `src/ingestion/extractors/youtube_extractor.py`. Implementar função que usa `yt-dlp` para transferir áudio de uma URL para a pasta `/tmp/` e devolve o caminho do ficheiro transferido.

## Descrição Técnica
Foi criado o subdiretório `src/ingestion/extractors/` (com `__init__.py`) e o arquivo `youtube_extractor.py` contendo a função `download_audio(url)`. A função utiliza `yt-dlp` para descarregar o melhor áudio disponível, converte-o para MP3 via pós-processador FFmpeg e devolve o caminho absoluto do ficheiro em `/tmp/`.

## Decisões de Implementação
- **Formato de saída:** MP3 a 192kbps — compatível com `faster-whisper` (T11/T12) sem conversão adicional.
- **Template de saída:** `{tempdir}/{video_id}.mp3` — o `video_id` extraído do `info` garante o nome previsível necessário para devolução do caminho.
- **Tratamento de erros:** `yt_dlp.utils.DownloadError` é capturado e re-lançado como `ValueError` com mensagem descritiva; erros inesperados são propagados após log.
- **Silêncio no terminal:** `quiet=True` e `no_warnings=True` evitam ruído no stdout do Streamlit.

## Estrutura Criada
```
src/ingestion/extractors/
├── __init__.py
└── youtube_extractor.py   # função pública: download_audio(url: str) -> str
```

## Contrato da Função `download_audio`
- **Entrada:** `url` (str) — URL válida do YouTube.
- **Saída:** caminho absoluto do ficheiro MP3 em `/tmp/` (ex: `/tmp/dQw4w9WgXcQ.mp3`).
- **Exceções:** `ValueError` para URL vazia ou falha de download; `FileNotFoundError` se o ficheiro não for encontrado após o download.
- **Dependência de pipeline:** O pipeline chamador (T13) é responsável por apagar o ficheiro após a transcrição.

# Resumo da Implementação - Tarefa T11

## Tarefa Executada
**T11:** Criar `src/ingestion/transcribers/local_whisper.py`. Implementar classe que inicializa o `faster-whisper`.

## Descrição Técnica
Foi criado o subdiretório `src/ingestion/transcribers/` (com `__init__.py`) e o arquivo `local_whisper.py` contendo a classe `WhisperTranscriber`. A classe encapsula a inicialização do modelo `faster-whisper` com configurações adequadas para execução local em Apple Silicon (M3, 16GB RAM).

## Decisões de Implementação
- **`MODEL_SIZE = "medium"`**: Equilibrio entre qualidade de transcrição e consumo de memória RAM. Pode ser ajustado para `"small"` se necessário.
- **`DEVICE = "cpu"` e `COMPUTE_TYPE = "int8"`**: Combinação validada para Apple Silicon via CPU, sem dependência de CUDA. A quantização `int8` reduz o consumo de memória durante a inferência.
- **Atributos de classe para as constantes de configuração**: Facilita a sobrescrita para testes ou ajuste futuro sem alterar o construtor.
- **Inicialização no `__init__`**: O modelo é carregado ao instanciar a classe; T12 adicionará o método de transcrição com a regra estrita de destruição do modelo após o uso.

## Estrutura Criada
```
src/ingestion/transcribers/
├── __init__.py
└── local_whisper.py   # classe pública: WhisperTranscriber
```

## Contrato da Classe `WhisperTranscriber` (T11)
- **`__init__()`**: Instancia `faster_whisper.WhisperModel` com `model_size="medium"`, `device="cpu"`, `compute_type="int8"` e atribui a `self.model`.
- **Exceções no init:** Qualquer falha no carregamento do modelo é logada e re-lançada.
- **Pendente (T12):** Implementação do método `transcribe(audio_path)` com regra estrita de limpeza de memória (`del self.model` + `gc.collect()`) antes de retornar a string transcrita.

# Resumo da Implementação - Tarefa T12

## Tarefa Executada
**T12:** No `local_whisper.py`, implementar a regra estrita de memória: após gerar a transcrição, o método deve executar `del self.model` e `import gc; gc.collect()` antes de devolver a string.

## Descrição Técnica
Foi adicionado o método `transcribe(audio_path)` à classe `WhisperTranscriber`. A implementação cumpre o KPI de **Zero OOM** definido no BLUEPRINT: o modelo é destruído e o GC é invocado via bloco `finally`, garantindo que a RAM seja libertada independentemente de sucesso ou falha na transcrição, antes que o pipeline inicie o SemanticChunker e os embeddings Ollama.

## Decisões de Implementação
- **`finally` em vez de `try/except` puro:** Garante que `del self.model` + `gc.collect()` sejam executados mesmo em caso de exceção durante a transcrição, evitando vazamento de memória em qualquer cenário.
- **`beam_size=5`:** Valor padrão do faster-whisper, equilibrando precisão e velocidade.
- **Join de segmentos:** O faster-whisper retorna um generator de segmentos; a junção com `" ".join(...)` materializa o generator antes da limpeza de memória.
- **`import os` interno ao método:** Mantém o import de `gc` no topo do módulo (usado exclusivamente neste método) e evita dependências desnecessárias no `__init__`.

## Contrato do Método `transcribe`
- **Entrada:** `audio_path` (str) — caminho absoluto de ficheiro de áudio existente.
- **Saída:** `str` — texto completo da transcrição (segmentos unidos por espaço).
- **Exceções:** `FileNotFoundError` se o ficheiro não existir; `RuntimeError` para falhas de transcrição.
- **Garantia de memória:** `self.model` é sempre destruído e `gc.collect()` é sempre chamado antes do retorno, via bloco `finally`.

# Resumo da Implementação - Tarefa T13

## Tarefa Executada
**T13:** Criar `src/ingestion/pipelines/youtube_pipeline.py`. Orquestrar o fluxo: Transferir áudio -> Transcrever -> Apagar áudio original -> Chamar `SemanticProcessor` -> Guardar no `VectorDB`.

## Descrição Técnica
Foi criado o subdiretório `src/ingestion/pipelines/` (com `__init__.py`) e o arquivo `youtube_pipeline.py` com a função pública `run(url, category)`. A função orquestra os 6 passos do pipeline em sequência estrita, respeitando a ordem de libertação de memória definida no BLUEPRINT.

## Decisões de Implementação
- **`_extract_title(url)`:** Função privada que faz uma chamada `extract_info(download=False)` ao yt-dlp para obter o título sem duplicar o download. Garante que o campo `title` dos metadados seja o nome real do vídeo e não a URL.
- **Remoção do áudio com `try/except OSError`:** O pipeline não aborta se o `os.remove` falhar (ex.: ficheiro já removido). É tratado como aviso, não como erro fatal.
- **`source_id = SHA256(url)`:** Cumpre o contrato definido em T09 — o identificador único é calculado a partir da fonte original (URL), não do conteúdo.
- **Ordem das instâncias:** `WhisperTranscriber` (e o seu modelo) é destruído dentro de `transcribe()` antes de `SemanticProcessor` e `VectorDB` serem instanciados, garantindo Zero OOM.

## Estrutura Criada
```
src/ingestion/pipelines/
├── __init__.py
└── youtube_pipeline.py   # função pública: run(url: str, category: str) -> int
```

## Contrato da Função `run`
- **Entrada:** `url` (str), `category` (str).
- **Saída:** `int` — número de chunks armazenados no ChromaDB.
- **Exceções:** propaga `ValueError` do extractor e erros do ChromaDB.

---

# Resumo da Implementação - Tarefas T14 e T15

## Tarefas Executadas
**T14:** Criar `src/services/chat_engine.py`. Criar classe `ChatAssistant` instanciando `ChatOllama`.
**T15:** No `ChatAssistant`, implementar a cadeia de RAG ligando o histórico de sessão (`InMemoryChatMessageHistory`), o prompt de sistema e a pesquisa vetorial.

## Descrição Técnica
Foi criado `src/services/chat_engine.py` com a classe `ChatAssistant`. A cadeia RAG é construída com 4 componentes LangChain encadeados e o prompt de sistema é injetado via `settings.py` (variável `SYSTEM_PROMPT`), cumprindo o critério de **agnosticismo de agente** do BLUEPRINT.

## Componentes da Cadeia RAG
1. **`create_history_aware_retriever`:** Reformula a query do utilizador em query independente do histórico antes de invocar o retriever, evitando buscas ambíguas com pronomes ou referências implícitas.
2. **`create_stuff_documents_chain`:** Constrói a resposta concatenando os chunks recuperados no prompt com `{context}`.
3. **`create_retrieval_chain`:** Une os dois anteriores num pipeline end-to-end.
4. **`RunnableWithMessageHistory`:** Envolve o RAG chain e injeta automaticamente o histórico de sessão correto via `session_id`.

## Decisões de Implementação
- **`SYSTEM_PROMPT` em `settings.py`:** Adicionada variável configurável via `.env`, com valor padrão funcional. Permite troca de persona sem alterar código.
- **`@st.cache_resource` em `app.py`:** O `ChatAssistant` é instanciado uma única vez por processo do servidor Streamlit, evitando re-inicialização do ChromaDB e do ChatOllama a cada rerun.
- **`get_response` como generator:** Itera sobre `.stream()` da chain e faz `yield` apenas do campo `"answer"` de cada chunk, compatível com `st.write_stream`.
- **`_sessions: dict[str, InMemoryChatMessageHistory]`:** Histórico isolado por `session_id`, permitindo múltiplos utilizadores simultâneos sem cruzamento de contexto.

## Contrato do Método `get_response`
- **Entrada:** `question` (str), `session_id` (str, padrão `"default"`).
- **Saída:** `Generator[str, None, None]` — fragmentos da resposta para `st.write_stream`.

---

# Resumo da Implementação - Tarefas T16, T17 e T18

## Tarefas Executadas
**T16:** Criar `app.py` com `st.set_page_config` e as duas primeiras abas.
**T17:** Aba YouTube — input de URL, selectbox de categoria, botão com `st.spinner`.
**T18:** Aba Chat — ciclo de renderização de mensagens, `st.chat_input`, `st.write_stream`.

## Descrição Técnica
Foi criado `app.py` na raiz do projeto, servindo como entrypoint do Streamlit. O ficheiro implementa as duas abas da Fase 1 e conecta a UI aos módulos de backend já implementados.

## Decisões de Implementação
- **`uuid.uuid4()` em `st.session_state`:** Garante um `session_id` único por aba de browser, mantendo históricos de conversa isolados entre utilizadores distintos.
- **Botão desativado (`disabled=not url.strip()`):** Impede submissões com campo de URL vazio sem exigir validação explícita extra.
- **`st.chat_input` + `st.chat_message`:** Padrão idiomático do Streamlit para interfaces de chat, com renderização automática de bolhas de mensagem.
- **`response = st.write_stream(...)`:** `st.write_stream` devolve a string completa após o stream terminar, que é então persistida em `st.session_state.messages` para re-renderização em reruns futuros.
- **`@st.cache_resource` no `get_assistant()`:** Evita que o `ChatAssistant` (e o ChromaDB + Ollama embeddings associados) sejam reinicializados a cada interação do utilizador.

## Estrutura Final da Fase 1
```
app.py                              # Entrypoint Streamlit
src/
├── config/settings.py              # LLM_MODEL, EMBEDDING_MODEL, CHROMA_PATH, SYSTEM_PROMPT
├── config/logger.py
├── database/chroma_wrapper.py      # VectorDB
├── ingestion/
│   ├── chunker.py                  # SemanticProcessor
│   ├── extractors/youtube_extractor.py
│   ├── transcribers/local_whisper.py
│   └── pipelines/youtube_pipeline.py
└── services/chat_engine.py         # ChatAssistant (RAG + histórico)
```

A **Fase 1** está completa. O sistema pode ser iniciado com `streamlit run app.py`.
