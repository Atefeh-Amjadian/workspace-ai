# Workspace AI

AI-powered Email Workflow Assistant built with FastAPI, PostgreSQL, Gmail API, and Ollama.

---

# Overview

Workspace AI is an intelligent email assistant platform designed to automate repetitive email management tasks.

The system integrates Gmail, AI-powered text processing, and workflow automation to help users manage emails more efficiently.

Current capabilities include:

* Synchronizing unread Gmail emails
* AI-generated email summaries
* Email classification (Urgent, Important, FYI, Spam)
* AI-generated draft replies
* Dashboard analytics
* Background AI processing
* Retry mechanism for failed AI tasks

---

# Screenshots

## Swagger API

![Swagger API](docs/images/swagger.png)

## Dashboard Statistics

![Dashboard](docs/images/dashboard.png)

## Retry Endpoint

![Retry Endpoint](docs/images/retry-endpoint.png)

---

# Features

## Gmail Integration

* Read unread Gmail messages
* Synchronize emails into PostgreSQL
* Prevent duplicate email imports

## AI Email Processing

* Generate concise email summaries
* Classify emails into categories:

  * Urgent
  * Important
  * FYI
  * Spam
* Generate draft replies

## Background Processing

AI tasks run in the background to keep API responses fast and responsive.

## Reliability Features

* AI processing status tracking
* Pending / Processing / Completed / Failed states
* Retry endpoint for failed or pending AI tasks

## Dashboard

Provides analytics such as:

* Total emails
* Urgent emails
* Important emails
* FYI emails
* Spam emails

---

# Architecture

```text
                Gmail API
                    │
                    ▼
         ┌─────────────────────┐
         │    FastAPI Backend  │
         └─────────┬───────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
 PostgreSQL             Ollama (Phi3)
 Database                Local LLM
        │                     │
        └──────────┬──────────┘
                   ▼
            Dashboard APIs
```

---

# Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic

## Database

* PostgreSQL

## AI

* Ollama
* Phi3 Mini

## Infrastructure

* Docker
* Docker Compose

## External Services

* Gmail API

---

# Project Structure

```text
workspace-ai/
│
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── credentials/
│   ├── requirements.txt
│   └── .env
│
├── docs/
│   └── images/
│
├── database/
│
├── docker-compose.yml
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Atefeh-Amjadian/workspace-ai.git

cd workspace-ai/backend
```

## Create Virtual Environment

```bash
python -m venv venv

source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file inside the backend directory:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/workspace_ai

OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=phi3:mini
```

---

# Running the Project

## Start PostgreSQL

```bash
docker compose up -d
```

## Start FastAPI

```bash
cd backend

source venv/bin/activate

uvicorn app.main:app --reload
```

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Gmail

```http
POST /emails/sync-gmail
```

Synchronize unread Gmail emails into PostgreSQL.

---

## Email Processing

```http
POST /emails/{id}/summarize
```

Generate email summary.

```http
POST /emails/{id}/classify
```

Classify email category.

```http
POST /emails/{id}/draft-reply
```

Generate AI draft reply.

```http
POST /emails/process-pending
```

Retry pending or failed AI processing tasks.

---

## Dashboard

```http
GET /dashboard/stats
```

Retrieve email analytics statistics.

---

# Reliability Features

The system includes:

* Background AI processing
* AI task status tracking
* Pending / Processing / Completed / Failed workflow
* Retry endpoint
* Database migrations using Alembic

---

# Future Improvements

* Telegram daily reports
* Gmail draft creation
* Celery + Redis task queue
* Automated email workflows
* RAG-based email search
* Calendar integration
* Multi-agent AI workflows

---

# Author

**Atefeh Amjadian**

GitHub:

https://github.com/Atefeh-Amjadian
