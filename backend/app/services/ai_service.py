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
        response = httpx.post(url, json=payload, timeout=120)
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