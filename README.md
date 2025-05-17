# Infra Copilot
Your infra-as-prompt for easy and fast Cloud Infrastructure manager, an **Agent** who can mange your Infra like your SRE and Cloud Engineer does.

Or you can say It's a buddy for SRE and CLoud Engineers.

----

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