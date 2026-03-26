
# PRD (Product Requirements Document)

**1. Visão Geral do Produto (VideoBrain V2)**
Um sistema de "Segundo Cérebro" Multimodal (PKM) construído do zero. Operando 100% offline (local-first) num Apple Silicon (M3, 16GB RAM). O sistema fará a ingestão de conteúdos diversos (YouTube, arquivos locais de mídia e documentos) transformando-os em embeddings armazenados no ChromaDB para consultas interativas via chat utilizando RAG avançado.

**2. UX e Fluxo de Interface (Desacoplamento)**
A interface será construída em Streamlit e dividida em 4 abas estritas:
* **Chat:** Interface de conversação com o modelo LLM, contendo histórico de sessão.
* **Ingestão YouTube:** Formulário para inserir uma URL, definir a "Categoria" e acionar o pipeline de download (`yt-dlp`) + transcrição (`faster-whisper`).
* **Ingestão Mídia Local:** Upload de arquivos de áudio/vídeo, seleção de "Categoria" e acionamento da transcrição.
* **Ingestão Documentos:** Upload de PDFs/Word, seleção de "Categoria" e acionamento do processamento via `docling`.

**3. Critérios de Sucesso (KPIs)**
* **Modularidade Extrema:** O código de ingestão do YouTube não deve compartilhar a mesma classe de execução do código de ingestão de PDFs.
* **Estabilidade de Hardware (Zero OOM):** O pipeline deve instanciar o modelo do Whisper, transcrever e, obrigatoriamente, destruir a instância na memória (via `del` e `gc.collect()`) antes de iniciar o processo de *Semantic Chunking* e vetorização no Ollama.
* **Agnosticismo de Agente:** O motor de chat deve ter um prompt de sistema injetado via arquivo de configuração ou variável, permitindo que a persona da IA seja alterada facilmente no futuro.

---
# TECH_SPEC (Especificação Técnica)

**1. Arquitetura de Pastas (Clean Greenfield)**
```text
/
├── app.py                  # Entrypoint do Streamlit (UI e Roteamento das Abas)
├── requirements.txt        # Dependências estritas
├── .env                    # Variáveis de ambiente
├── data/
│   └── chromadb/           # Persistência local do banco vetorial
└── src/
    ├── config/             # Configurações globais (settings.py)
    ├── database/           # Wrapper do ChromaDB
    ├── ingestion/          # Módulos de ingestão (isolados por tipo)
    │   ├── youtube.py
    │   ├── local_media.py
    │   ├── document.py
    │   └── chunker.py      # Lógica central do SemanticChunker
    └── services/           # Motor RAG e LLM
        └── chat_engine.py
```

**2. Stack e Dependências**
- `streamlit` (Frontend)
- `langchain`, `langchain-ollama`, `langchain-chroma`, `langchain-experimental` (Core RAG)
- `faster-whisper` (Transcrição local)
- `yt-dlp` (Download web)
- `docling` (Parseamento de documentos complexos)

**3. Modelagem de Metadados (ChromaDB)** Cada _Document_ armazenado conterá a seguinte estrutura no dicionário `metadata`:
- `source_id`: Identificador único (Hash SHA-256 do arquivo ou URL).
- `source_type`: Origem (`youtube`, `local_media`, `pdf`, `docx`).
- `category`: Tema definido na interface (ex: Estudos, Finanças).
- `title`: Nome do arquivo ou título do vídeo.

## TASKS (Plano de Ação de Implantação Progressiva)

**Fase 1: Fundação, Chat e MVP do YouTube (Primeira Implantação)**
* [x] **T01:** Criar estrutura de pastas (`src/config`, `src/database`, `src/ingestion`, `src/services`, `data/chromadb`).
* [x] **T02:** Criar o ficheiro `requirements.txt` com todas as dependências do projeto e instalar no ambiente virtual.
* [x] **T03:** Criar ficheiro `.env` com as configurações (ex: `LLM_MODEL="gemma3n:e4b"`, `EMBEDDING_MODEL="embeddinggemma:300m"`, `CHROMA_PATH="data/chromadb"`).
* [x] **T04:** Criar `src/config/settings.py` para carregar as variáveis de ambiente utilizando a biblioteca `os` ou `pydantic-settings`.
* [x] **T05:** Criar `src/config/logger.py` para estabelecer um padrão de registos (logs) no terminal (INFO, DEBUG, ERROR).
* [x] **T06:** Criar `src/database/chroma_wrapper.py`. Instanciar a classe `VectorDB` com inicialização do ChromaDB acoplado ao `OllamaEmbeddings`.
* [x] **T07:** Na classe `VectorDB`, implementar o método `add_chunks(chunks)` e o método `search(query, k=5)`.
* [x] **T08:** Criar `src/ingestion/chunker.py`. Implementar a classe `SemanticProcessor` configurando o `SemanticChunker` da LangChain.
* [x] **T09:** No `SemanticProcessor`, implementar o método `process_and_format(text, metadata_dict)` que fatia o texto e injeta `source_id`, `source_type`, `category` e `title` em cada fragmento.
* [x] **T10:** Criar `src/ingestion/extractors/youtube_extractor.py`. Implementar função que usa `yt-dlp` para transferir áudio de uma URL para a pasta `/tmp/` e devolve o caminho do ficheiro transferido.
* [x] **T11:** Criar `src/ingestion/transcribers/local_whisper.py`. Implementar classe que inicializa o `faster-whisper`.
* [x] **T12:** No `local_whisper.py`, implementar a regra estrita de memória: após gerar a transcrição, o método deve executar `del self.model` e `import gc; gc.collect()` antes de devolver a string.
* [x] **T13:** Criar `src/ingestion/pipelines/youtube_pipeline.py`. Orquestrar o fluxo: Transferir áudio -> Transcrever -> Apagar áudio original -> Chamar `SemanticProcessor` -> Guardar no `VectorDB`.
* [x] **T14:** Criar `src/services/chat_engine.py`. Criar classe `ChatAssistant` instanciando `ChatOllama`.
* [x] **T15:** No `ChatAssistant`, implementar a cadeia (chain) de RAG ligando o histórico de sessão (`InMemoryChatMessageHistory`), o prompt de sistema e a pesquisa vetorial.
* [x] **T16:** Criar `app.py`. Configurar `st.set_page_config` e criar as duas primeiras abas: `tab1, tab2 = st.tabs(["Chat", "YouTube"])`.
* [x] **T17:** Em `app.py` (aba YouTube), implementar input de URL, selectbox de categoria e botão que aciona o `youtube_pipeline.py` com `st.spinner`.
* [x] **T18:** Em `app.py` (aba Chat), implementar o ciclo de renderização de mensagens, input do utilizador e ligação com o `ChatAssistant.get_response` usando `st.write_stream`.

**Fase 2: Expansão para Documentos (Segunda Implantação)**
* [ ] **T19:** Criar `src/ingestion/extractors/doc_extractor.py`. Implementar extração de texto de PDF/Docx utilizando a biblioteca `docling`.
* [ ] **T20:** Criar `src/ingestion/pipelines/document_pipeline.py`. Orquestrar o fluxo: Ler ficheiro -> Extrair texto via Docling -> Chamar `SemanticProcessor` -> Guardar no `VectorDB` com `source_type="document"`.
* [ ] **T21:** Atualizar `app.py`. Adicionar a aba `📄 Documentos`. Inserir um `st.file_uploader` e ligar o ficheiro recebido ao `document_pipeline.py`.

**Fase 3: Expansão para Mídia Local (Terceira Implantação)**
* [ ] **T22:** Criar `src/ingestion/pipelines/local_media_pipeline.py`. Orquestrar fluxo: Guardar ficheiro recebido no disco (`/tmp/`) -> Transcrever via `local_whisper.py` (com limpeza de memória) -> Apagar ficheiro -> Chamar `SemanticProcessor` -> Guardar no `VectorDB`.
* [ ] **T23:** Atualizar `app.py`. Adicionar a aba `📼 Mídia Local`. Inserir `st.file_uploader` (focado em áudio/vídeo) e ligar ao `local_media_pipeline.py`. Homologar o sistema completo.