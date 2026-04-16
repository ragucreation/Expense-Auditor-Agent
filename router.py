from extractor import extract_expense_data
from policy_engine import audit_expense
import requests
import json
from prompts import RECOMMENDER_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3-vl:8b"

def run_expense_audit(image_pil=None, text_input=None):
    """
    Complete workflow: Extraction -> Audit -> Final Recommendation
    """
    # 1. Extract
    extracted_data = extract_expense_data(image_pil, text_input)
    if not extracted_data:
        return {"error": "Could not extract data from the provided source."}

    # 2. Audit
    audit_report = audit_expense(extracted_data)

    # 3. Final Recommendation (Short summary)
    payload = {
        "model": MODEL_NAME,
        "prompt": RECOMMENDER_PROMPT.format(audit_report=json.dumps(audit_report)),
        "stream": False
    }
    
    try:
        recommendation_res = requests.post(OLLAMA_URL, json=payload, timeout=30)
        recommendation = recommendation_res.json().get("response", "").strip()
    except:
        recommendation = "Manual review recommended due to system timeout."

    return {
        "extracted_data": extracted_data,
        "audit_report": audit_report,
        "recommendation": recommendation
    }
