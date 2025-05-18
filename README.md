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
