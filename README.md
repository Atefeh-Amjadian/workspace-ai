# Workspace AI

## Overview

Workspace AI is an AI-powered email assistant platform designed to automate repetitive email management tasks.

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

## Features

### Gmail Integration

* Read unread Gmail messages
* Synchronize emails into PostgreSQL
* Prevent duplicate email imports

### AI Email Processing

* Generate concise email summaries
* Classify emails into categories:

  * Urgent
  * Important
  * FYI
  * Spam
* Generate draft replies

### Background Processing

AI tasks run in the background to keep API responses fast and responsive.

### Reliability Features

* AI processing status tracking
* Pending / Processing / Completed / Failed states
* Retry endpoint for failed or pending AI tasks

### Dashboard

Provides analytics such as:

* Total emails
* Urgent emails
* Important emails
* FYI emails
* Spam emails

---

## Architecture

Gmail API

↓

FastAPI Backend

↓

PostgreSQL Database

↓

Ollama Local LLM

↓

Dashboard & API Endpoints

---

## Tech Stack

Backend:

* Python
* FastAPI
* SQLAlchemy
* Alembic

Database:

* PostgreSQL

AI:

* Ollama
* Phi3 Mini

Infrastructure:

* Docker
* Docker Compose

External Services:

* Gmail API

---

## Project Structure

backend/

├── app/

│ ├── api/

│ ├── core/

│ ├── db/

│ ├── models/

│ ├── schemas/

│ └── services/

├── alembic/

├── credentials/

├── requirements.txt

└── .env

---

## Installation

### Clone Repository

git clone <repository-url>

cd workspace-ai/backend

### Create Virtual Environment

python -m venv venv

source venv/bin/activate

### Install Dependencies

pip install -r requirements.txt

---

## Environment Variables

Create a .env file:

DATABASE_URL=postgresql://user:password@localhost:5432/workspace_ai

OLLAMA_BASE_URL=http://localhost:11434

OLLAMA_MODEL=phi3:mini

---

## Running the Project

### Start PostgreSQL

docker compose up -d

### Start FastAPI

uvicorn app.main:app --reload

### Swagger UI

http://127.0.0.1:8000/docs

---

## API Endpoints

### Gmail

POST /emails/sync-gmail

### Email Processing

POST /emails/{id}/summarize

POST /emails/{id}/classify

POST /emails/{id}/draft-reply

POST /emails/process-pending

### Dashboard

GET /dashboard/stats

---

## Reliability Features

The system includes:

* Background AI processing
* AI task status tracking
* Retry mechanism
* Database migrations using Alembic

---

## Future Improvements

* Telegram daily reports
* Gmail draft creation
* Celery + Redis task queue
* Automated email workflows
* RAG-based email search
* Calendar integration
* Multi-agent AI workflows

---

## Author

Atefeh Amjadian

GitHub:
https://github.com/Atefeh-Amjadian
