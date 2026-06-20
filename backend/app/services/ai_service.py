import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


def generate_text(prompt: str) -> str:
    url = f"{settings.ollama_base_url}/api/generate"

    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = httpx.post(
            url,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()

        data = response.json()

        return data["response"].strip()

    except httpx.ConnectError:
        logger.error("Could not connect to Ollama")
        raise RuntimeError("AI service is unavailable")

    except httpx.TimeoutException:
        logger.error("Ollama request timed out")
        raise RuntimeError("AI service timed out")

    except httpx.HTTPError as error:
        logger.error("Ollama HTTP error: %s", error)
        raise RuntimeError("AI service is unavailable")

    except KeyError:
        logger.error("Unexpected Ollama response format")
        raise RuntimeError("AI service returned an invalid response")


def summarize_text(
    subject: str,
    sender: str,
    snippet: str | None,
    category: str,
) -> str:
    prompt = f"""
You are an email assistant.

Task:
Write exactly ONE short sentence summarizing the email.

Email:
Subject: {subject}
Sender: {sender}
Snippet: {snippet or "No email content available"}
Category: {category}

Rules:
- Maximum 15 words.
- One sentence only.
- No explanations.
- No reasoning.
- No bullet points.
- No introductions.
- No conclusions.
- Return only the summary.
"""

    summary = generate_text(prompt)

    summary = summary.split("\n")[0].strip()

    return summary[:200]


def classify_text(
    subject: str,
    sender: str,
    snippet: str | None,
    summary: str | None,
) -> str:
    prompt = f"""
You are an email classification assistant.

Classify the email into exactly one of these categories:

urgent
important
fyi
spam

Email:
Subject: {subject}
Sender: {sender}
Snippet: {snippet or "No email content available"}
Summary: {summary or "No summary available"}

Rules:
- Return only one word.
- Do not explain.
- Do not use punctuation.
- Choose "urgent" only if immediate action is required.
- Choose "important" if it matters but is not urgent.
- Choose "fyi" if it is informational.
- Choose "spam" if it is promotional, irrelevant, or suspicious.
"""

    category = generate_text(prompt).lower().strip()

    allowed_categories = {
        "urgent",
        "important",
        "fyi",
        "spam",
    }

    if category not in allowed_categories:
        return "fyi"

    return category


def generate_reply(
    subject: str,
    sender: str,
    snippet: str | None,
    category: str,
    summary: str | None,
) -> str:
    prompt = f"""
You are an email assistant.

Write a short, natural, professional reply to the email below.

Email:
Subject: {subject}
Sender: {sender}
Snippet: {snippet or "No email content available"}
Category: {category}
Summary: {summary or "No summary available"}

Rules:
- Maximum 3 sentences.
- Do not include a subject line.
- Do not include placeholders like [Your Name].
- Do not invent details.
- Use clear and simple English.
- Return only the reply.
"""

    return generate_text(prompt)