import requests

# Ollama API endpoint (runs locally on your machine)
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


def ask_gemini(prompt):
    """
    Send prompt to local Ollama instance running Llama2
    No API key needed - runs completely locally!
    """
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7,
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=data, timeout=300)

        if response.status_code != 200:
            raise ValueError(f"Ollama Error: {response.status_code} - {response.text}")

        result = response.json()
        return result["response"].strip()

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Cannot connect to Ollama. Make sure:\n"
            "1. Ollama is installed from https://ollama.ai/\n"
            "2. Ollama is running (should start automatically)\n"
            "3. A model is downloaded: ollama pull llama2\n"
            "4. It's listening on http://localhost:11434"
        )