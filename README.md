# Infra Copilot
Your infra-as-prompt for easy and fast Cloud Infrastructure manager, an **Agent** who can mange your Infra like your SRE and Cloud Engineer does.

Or you can say It's a buddy for SRE and CLoud Engineers.

----

## Directory Structure

```bash
llm_orchestrator/
├── api/                    # FastAPI route definitions
│   └── v1/
│       └── routes.py
├── agents/                 # Modular agents
│   └── base.py
│   └── terraform_agent.py
├── core/                   # Core utilities, DI, config
│   └── config.py
│   └── di.py
│   └── mcp_client.py
├── llms/                   # LLM providers (OpenAI, Groq, etc.)
│   └── base.py
│   └── openai_provider.py
├── services/               # Business logic orchestration
│   └── agent_orchestrator.py
├── state_engine/           # FSM/Graph transitions
│   └── node.py
│   └── transition_engine.py
├── terraform_docs/         # Ingestion, embedding, search
│   └── doc_loader.py
│   └── embedder.py
├── tools/                  # CLI tool wrappers (e.g., Terraform)
│   └── terraform_runner.py
├── schemas/                # Pydantic models
│   └── llm.py
│   └── agent.py
├── tests/                  # Unit & integration tests
│   └── test_orchestration.py
├── main.py                 # FastAPI app entry
├── requirements.txt
├── pyproject.toml / setup.py
└── README.md
```


## Structure and Architecture
```bash
            ┌────────────────────────────┐
            │    User Prompt Input       │
            │ (Web UI or CLI Interface)  │
            └────────────┬───────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │   Prompt Parser Agent      │
            │ (LangChain + LLM Model)    │
            └────────────┬───────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │  Infra Blueprint Generator │
            │  (JSON/YAML Schema Output) │
            └────────────┬───────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │  Terraform Code Generator  │
            └────────────┬───────────────┘
                         │
                         ▼
         ┌────────────────────────────────────┐
         │    Infra Executor (TF Plan/Apply)  │
         │ (Backend: FastAPI + Shell Runner)  │
         └────────────┬────────────┬────────-─┘
                      │            │
                      ▼            ▼
            Terraform Logs   Infra State Manager
             & Feedback        (Postgres/Redis)
                      │
                      ▼
           ┌────────────────────────────┐
           │  User Approval Interface   │
           └────────────────────────────┘
```


## 🔍 Docs Engine for Infra-Copilot

This module powers **Retrieval-Augmented Generation (RAG)** for Infra-Copilot by enabling semantic search over AWS and Terraform documentation. It allows agents to **find and inject relevant documentation context** into LLM prompts using embeddings and a vector store.

---

## 📦 What It Does

- 🔎 **Scrapes official AWS/Terraform docs**
- ✂️ **Chunks the text** into manageable pieces
- 🧠 **Embeds chunks** using `sentence-transformers`
- 💾 **Stores embeddings** in Weaviate (a fast vector DB)
- 🎯 **Retrieves the most relevant chunks** when a user prompt mentions services like `S3`, `Lambda`, etc.

---

## 🧱 Directory Structure

docs_engine/
├── base_loader.py         # Base class for all doc loaders
├── chunker.py             # Splits large text into chunks
├── embedder.py            # Converts chunks to embeddings and stores them
├── retriever.py           # Pulls top-k relevant chunks using semantic search
├── weaviate_client.py     # Manages Weaviate connection & schema
├── loaders/
│   ├── aws_loader.py      # Extracts and parses AWS docs
│   ├── terraform_loader.py# (Stub) Extracts Terraform Registry docs

---

## 🚀 How It Works

1. **Load a doc page** (e.g. AWS EC2 Monitoring Guide)
2. **Chunk it** into readable paragraphs
3. **Embed each chunk** using `MiniLM` transformer
4. **Store** chunks + metadata in Weaviate under `DocumentChunk` class
5. **Query** docs dynamically based on user input or resource type

---

## 📋 Example Usage

```python
from docs_engine.loaders.aws_loader import AWSLoader
from docs_engine.chunker import chunk_text
from docs_engine.embedder import embed_and_store

url = "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-instances.html"
text = AWSLoader().load(url)
chunks = chunk_text(text)
embed_and_store(chunks, source_url=url)

To retrieve docs for a prompt like “create an EC2 with Lambda and S3”:

```python
from docs_engine.retriever import get_context_for_prompt

chunks = get_context_for_prompt("create ec2 with lambda and s3")
for c in chunks:
    print(c.content)
```

## 🧠 Vector DB: Weaviate
-	💡 Fully open-source
-   🔍 Fast semantic search
-	🧱 Schema supports service, topic, chunk range, etc.
-	🏷️ Multi-tenant enabled

Start Weaviate locally with Docker:

```bash
docker run -d -p 8080:8080 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  semitechnologies/weaviate
```

## 🔧 Extending Support

Want to support GCP or Azure docs?

✅ Just add a new loader in loaders/ that inherits from BaseDocLoader.

⸻

## 🧩 Coming Soon
-	Terraform Registry document ingestion
-	Cost-aware doc filtering
-	Automatic doc refresh cron
-	Live context API: /api/v1/docs/retrieve

⸻

## 🧑‍💻 Contributing

Pull requests, new loaders, and improvement ideas are welcome!
This engine is a key module of the larger Infra-Copilot project.

⸻

## 📜 License

MIT – use it, fork it, scale it.
Docs belong to their respective cloud providers.
