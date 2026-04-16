import yaml
import requests
import json
from prompts import AUDITOR_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3-vl:8b"

def load_policy(path="policy.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def audit_expense(extracted_data, policy_path="policy.yaml"):
    """
    Combines deterministic rules (YAML) with LLM reasoning (Auditor Prompt).
    """
    policy = load_policy(policy_path)
    
    # Enrich prompt with policy context
    full_prompt = AUDITOR_PROMPT.format(
        extracted_data=json.dumps(extracted_data, indent=2),
        policy_rules=json.dumps(policy, indent=2)
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        # The LLM performs the comparative audit
        return json.loads(result.get("response", "{}"))
    except Exception as e:
        print(f"Audit Error: {e}")
        return {
            "overall_status": "error",
            "compliance_score": 0,
            "violations": [{"rule": "System", "severity": "high"}],
            "justification": f"Failed to perform audit: {str(e)}"
        }
