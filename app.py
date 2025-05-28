import pandas as pd
from docxtpl import DocxTemplate
from datetime import date
import streamlit as st
import io
import zipfile

st.set_page_config(page_title="KOC Contract Generator", layout="centered", page_icon="📝")

st.markdown("""
<style>
    .main {
        background-color: #f9f9fb;
        font-family: 'Segoe UI', sans-serif;
    }
    .title {
        font-size: 2.2em;
        font-weight: bold;
        color: #4a4a4a;
    }
    .subtitle {
        font-size: 1.1em;
        color: #6c6c6c;
    }
    .stFileUploader > label {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title">📄 KOC Contract Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Easily generate influencer contracts in bulk from a CSV and DOCX template</div>', unsafe_allow_html=True)
st.markdown("---")

# Upload section
col1, col2 = st.columns(2)
with col1:
    uploaded_csv = st.file_uploader("📑 Upload CSV File", type=["csv"])
with col2:
    uploaded_template = st.file_uploader("📄 Upload Word Template (.docx)", type=["docx"])

# Process files
if uploaded_csv and uploaded_template:
    st.success("✅ Files uploaded successfully!")
    df = pd.read_csv(uploaded_csv)
    df.columns = df.columns.str.strip()
    today = date.today().isoformat()
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        for index, row in df.iterrows():
            try:
                template = DocxTemplate(uploaded_template)

                context = {
                    'Influencer_name': row['Name'],
                    'Influencer_email': row['Email'],
                    'Influencer_contact': row['Contact'],
                    'Influencer_address': row['Address'],
                    'platform': row['Platform'],
                    'platform_username': row['Platform username'],
                    'Influencer_links': row['Links'],
                    'promotion_date': row['Promotion date'],
                    'video_rate': row['video rate'],
                    'bonus_info': row['bonus info'],
                    'payment_method': row['Payment method'],
                    'payment_information': row['Payment Info'],
                    'payment_charges': row['payment charges']
                }

                template.render(context)

                safe_name = row['Name'].replace(" ", "_").replace("/", "-")
                filename = f'FW-ARETIS_{safe_name}_{today}.docx'

                doc_stream = io.BytesIO()
                template.save(doc_stream)
                doc_stream.seek(0)

                zip_file.writestr(filename, doc_stream.read())

            except Exception as e:
                st.error(f"❌ Error processing {row.get('Name', f'Row {index}')} (row {index}): {e}")

    zip_buffer.seek(0)
    st.markdown("### ✅ All contracts generated!")
    st.download_button("📥 Download ZIP of All Contracts", zip_buffer, file_name=f"KOC_Contracts_{today}.zip", mime="application/zip")

else:
    st.info("⬆️ Upload both files above to get started.")
