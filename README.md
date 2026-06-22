# Workspace AI

AI-powered workspace assistant built with FastAPI, PostgreSQL, Ollama, Gmail API, and Telegram Bot API.

Workspace AI helps automate email workflows by synchronizing Gmail messages, storing them in a database, processing them with local AI models, generating summaries and draft replies, and delivering intelligent reports through Telegram.

---

## Features

### Gmail Integration

* Sync unread emails from Gmail
* Store emails in PostgreSQL
* Prevent duplicate email imports

### Email Dashboard

* Web-based email dashboard
* View synced emails
* Email statistics overview
* Email detail page

### AI Processing

* AI email summarization
* AI email classification
* AI-generated draft replies
* Local LLM processing using Ollama

### Telegram Integration

* Send Telegram notifications
* Send email summary reports
* Smart email brief generation

### Agent Workflow

* One-click email agent execution
* Gmail synchronization workflow
* Email processing workflow
* Telegram reporting workflow

---

## Architecture

```text
Gmail API
    ↓
Email Sync Service
    ↓
PostgreSQL
    ↓
AI Processing (Ollama)
    ├── Summarization
    ├── Classification
    └── Draft Reply Generation
    ↓
Telegram Notifications
    ↓
Email Agent Workflow
```

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic

### AI

* Ollama
* Phi-3 Mini

### Integrations

* Gmail API
* Telegram Bot API

### Infrastructure

* Docker
* Docker Compose

---

## Current Functionality

Implemented:

* Gmail synchronization
* Email storage
* Email dashboard
* Email statistics
* AI summarization
* AI classification
* Draft reply generation
* Telegram notifications
* Smart email reports
* Email agent workflow

---

## Future Roadmap

### Agent Memory

* Agent execution history
* Run tracking
* State management

### Background Processing

* Celery
* Redis
* Worker queues

### Advanced Agents

* Multi-agent workflows
* Autonomous task execution
* Decision-making agents

### Knowledge Systems

* RAG integration
* Internal knowledge base
* Semantic search

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/Atefeh-Amjadian/workspace-ai.git
cd workspace-ai
```

Create environment variables:

```env
DATABASE_URL=
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini

GMAIL_CREDENTIALS_FILE=
GMAIL_TOKEN_FILE=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Run the application:

```bash
docker compose up --build
```

Or locally:

```bash
uvicorn app.main:app --reload
```

---

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Project Status

Active Development 🚀

Current Version:

* Gmail Integration
* AI Email Processing
* Telegram Reporting
* Agent Workflow

Next Milestone:

* Agent Memory
* Celery + Redis
* Multi-Agent Architecture
