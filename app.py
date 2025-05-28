import pandas as pd
import streamlit as st
from docxtpl import DocxTemplate
import io
from datetime import date

st.set_page_config(page_title="KOC Contract Generator", layout="centered", page_icon="📝")

st.title("📝 KOC Contract Generator")

mode = st.radio("Choose Input Mode", ["Upload CSV for Bulk", "Manual Entry for Single Contract"])

uploaded_template = st.file_uploader("📄 Upload Word Template (.docx)", type=["docx"])

if mode == "Upload CSV for Bulk":
    uploaded_csv = st.file_uploader("📑 Upload CSV File", type=["csv"])
    # Keep existing CSV logic here...

elif mode == "Manual Entry for Single Contract":
    if uploaded_template:
        # Load column headers from your uploaded CSV
        sample_df = pd.read_csv("/mnt/data/Contract  - KOC.csv", nrows=1)
        sample_df.columns = sample_df.columns.str.strip()

        st.subheader("✍️ Enter Contract Details")

        # Create a form dynamically based on CSV columns
        context = {}
        for col in sample_df.columns:
            key = col.strip()
            if "date" in key.lower():
                context[key] = st.date_input(key)
            elif "rate" in key.lower() or "charges" in key.lower():
                context[key] = st.number_input(key, step=1.0)
            else:
                context[key] = st.text_input(key)

        if st.button("📄 Generate Contract"):
            try:
                template = DocxTemplate(uploaded_template)

                template.render(context)

                doc_stream = io.BytesIO()
                template.save(doc_stream)
                doc_stream.seek(0)

                st.download_button(
                    "📥 Download Contract",
                    doc_stream,
                    file_name=f"FW-ARETIS_{context.get('Name', 'Contract')}_{date.today().isoformat()}.docx"
                )
            except Exception as e:
                st.error(f"❌ Error generating contract: {e}")
    else:
        st.info("⬆️ Please upload a DOCX template to enable manual input.")
