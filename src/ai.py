
from openai import OpenAI
from src.config import GROQ_API_KEY, GROQ_MODEL


def ask_ai(
    prompt: str,
    system: str = "You are a clear, accurate study assistant.",
    provider=None,
) -> str:
    """Generate a response using Groq only."""

    if provider and str(provider).strip().lower() != "groq":
        raise RuntimeError(
            "StudyFlow AI is configured to use Groq only."
        )

    if not GROQ_API_KEY:
        raise RuntimeError(
            "Groq API key is missing. Add GROQ_API_KEY "
            "to the .env file in your project folder."
        )

    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        timeout=45.0,
        max_retries=0,
    )

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )

        if not response.choices:
            raise RuntimeError("Groq returned no response choices.")

        result = response.choices[0].message.content

        if not result or not result.strip():
            raise RuntimeError("Groq returned an empty response.")

        print("STUDYFLOW AI: Successfully generated using Groq.")
        return result.strip()

    except Exception as error:
        message = str(error).replace(
            GROQ_API_KEY, "[REDACTED]"
        )

        print(
            f"STUDYFLOW GROQ ERROR: "
            f"{type(error).__name__}: {message}"
        )

        raise RuntimeError(
            f"Groq request failed: {type(error).__name__}: {message}"
        ) from error
