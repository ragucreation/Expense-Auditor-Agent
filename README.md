# Expense-Auditor-Agent
Build an intelligent agent that extracts data from receipts/expense reports and audits them against a configurable policy.yaml.

User Review Required
IMPORTANT

This plan assumes you have Ollama running locally with the qwen3-vl:8b model, as configured in the previous project. We will be processing images (png, jpg) and text reports. PDF processing would require an additional library (pdf2image or similar).

Proposed Changes
We will build the system across several modules to ensure maintainability and separation of concerns.

Phase 1: Configuration & Prompts
[NEW] 
policy.yaml
Defines the rules for the auditor (limits, required categories, etc.).

[NEW] 
prompts.py
Centralizes the 3 core prompts:

Extractor Prompt: For vision-based data extraction.
Auditor Prompt: For comparing data against the policy summary.
Recommender Prompt: For generating final approvals/rejections with justifications.
Phase 2: Core Logic Modules
[NEW] 
extractor.py
Handles the interaction with the LLM to convert images/text into structured JSON data.

[NEW] 
policy_engine.py
Loads policy.yaml and performs deterministic checks (e.g., math-based limit checks) combined with LLM reasoning for fuzzy interpretation.

[NEW] 
router.py
Orchestrates the workflow: Input -> Extractor -> Policy Engine -> Final Output.

Phase 3: Application & Interface
[NEW] 
main.py
A Streamlit-based dashboard to upload reports, view violations in real-time, and download the audit summary.

[NEW] 
requirements.txt
Dependencies: streamlit, PyYAML, Pillow, requests.

Open Questions
OCR Specifics: Do you want to support multi-line item extraction (e.g., every single item on a grocery bill) or just the total amount and category?
PDF Support: Should we include pdf2image to allow uploading .pdf files as well? It requires the poppler system dependency.
Verification Plan
Automated Tests
Create a mock extraction result and run it against the policy_engine to ensure it flags a $150 meal when the limit is $75.
Test LLM connectivity using a simple health check script.
Manual Verification
Upload a "clean" receipt (within policy).
Upload a "violation" receipt (e.g., alcohol detected, over limit).
Verify the flags appear correctly in the Streamlit UI.
