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
    # Your existing CSV bulk logic goes here

elif mode == "Manual Entry for Single Contract":
    st.markdown("Use the form below to input contract details manually.")

    # Load column headers from the uploaded CSV to generate form fields
    try:
        sample_df = pd.read_csv("/mnt/data/Contract  - KOC.csv", nrows=1)
        sample_df.columns = sample_df.columns.str.strip()
        columns = sample_df.columns.tolist()
    except Exception:
        st.warning("⚠️ Could not read CSV for field reference. Using fallback.")
        columns = ["Name", "Email", "Start Date", "End Date", "Rate", "Platform", "Notes"]

    if uploaded_template:
        with st.form("manual_form"):
            st.subheader("🧾 Contract Details Form")

            context = {}
            for col in columns:
                key = col.strip()
                if "date" in key.lower():
                    context[key] = st.date_input(key, value=date.today())
                elif any(term in key.lower() for term in ["rate", "charges", "amount"]):
                    context[key] = st.number_input(key, min_value=0.0, step=1.0)
                else:
                    context[key] = st.text_input(key)

            submit = st.form_submit_button("📄 Generate Contract")

        if submit:
            try:
                template = DocxTemplate(uploaded_template)

                template.render(context)

                doc_stream = io.BytesIO()
                template.save(doc_stream)
                doc_stream.seek(0)

                st.success("✅ Contract generated successfully!")
                st.download_button(
                    "📥 Download Contract",
                    doc_stream,
                    file_name=f"FW-ARETIS_{context.get('Name', 'Contract')}_{date.today().isoformat()}.docx"
                )
            except Exception as e:
                st.error(f"❌ Error generating contract: {e}")
    else:
        st.info("⬆️ Please upload a DOCX template to continue.")
