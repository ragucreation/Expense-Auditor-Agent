import requests
import json
import base64
from io import BytesIO
from prompts import EXTRACTOR_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3-vl:8b"

def extract_expense_data(image_pil=None, text_input=None):
    """
    Uses LLM to extract structured JSON from receipt image or text.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": EXTRACTOR_PROMPT,
        "stream": False,
        "format": "json"
    }

    if text_input:
        payload["prompt"] += f"\n\nContext: {text_input}"

    if image_pil:
        buffered = BytesIO()
        image_pil.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        payload["images"] = [img_str]

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        
        # Parse the JSON response from the LLM
        return json.loads(result.get("response", "{}"))
    except Exception as e:
        print(f"Extraction Error: {e}")
        return None
