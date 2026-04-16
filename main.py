import streamlit as st
from PIL import Image
from router import run_expense_audit
import json

st.set_page_config(page_title="Expense Auditor AI", page_icon="🧾", layout="wide")

st.title("🧾 AI Expense Auditor")
st.markdown("Automated compliance review for employee expense reports.")

# Sidebar for metadata/policy status
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("Policy: `Corporate Travel & Expense v1.0` Loaded.")
    if st.button("Refresh Policy Cache"):
        st.success("Policy reloaded!")

# Main Tabs
tab1, tab2 = st.tabs(["📤 Upload & Audit", "📋 Policy View"])

with tab2:
    st.header("Current Active Policy")
    try:
        with open("policy.yaml", "r") as f:
            st.code(f.read(), language="yaml")
    except:
        st.error("Policy file not found.")

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. Submission")
        upload_type = st.radio("Source Type", ["Receipt Image", "Textual Report"])
        
        source_data = None
        if upload_type == "Receipt Image":
            source_data = st.file_uploader("Upload Receipt", type=["jpg", "jpeg", "png"])
            if source_data:
                img = Image.open(source_data)
                st.image(img, caption="Uploaded Image", use_container_width=True)
        else:
            source_data = st.text_area("Paste Expense Report Text", height=200)

        if st.button("Run Audit 🚀", use_container_width=True):
            if source_data:
                with st.spinner("Analyzing and auditing..."):
                    # Process based on type
                    if upload_type == "Receipt Image":
                        results = run_expense_audit(image_pil=Image.open(source_data))
                    else:
                        results = run_expense_audit(text_input=source_data)
                    
                    st.session_state['last_audit'] = results
            else:
                st.warning("Please provide a source for analysis.")

    with col2:
        st.subheader("2. Audit Results")
        if 'last_audit' in st.session_state:
            res = st.session_state['last_audit']
            
            if "error" in res:
                st.error(res["error"])
            else:
                # 1. Recommendation
                st.success(f"**Action:** {res['recommendation']}")
                
                # 2. Status Metric
                status = res['audit_report'].get('overall_status', 'N/A').upper()
                score = res['audit_report'].get('compliance_score', 0)
                
                mc1, mc2 = st.columns(2)
                mc1.metric("Compliance Status", status)
                mc2.metric("Compliance Score", f"{score}%")
                
                # 3. Violations
                st.markdown("### 🚩 Flags & Violations")
                violations = res['audit_report'].get('violations', [])
                if not violations:
                    st.write("✅ No policy violations detected.")
                else:
                    for v in violations:
                        st.error(f"**{v.get('rule', 'Unknown')}:** Severity {v.get('severity', 'Low')}")
                
                # 4. Extracted Data
                with st.expander("🔍 View Extracted Data"):
                    st.json(res['extracted_data'])
                
                with st.expander("📄 Full Audit Justification"):
                    st.write(res['audit_report'].get('justification', "No justification provided."))
        else:
            st.info("Upload a report and run the audit to see results here.")
