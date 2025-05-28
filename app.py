import pandas as pd
from docxtpl import DocxTemplate
from datetime import date
import streamlit as st
import io
import zipfile

st.set_page_config(page_title="KOC Contract Generator", layout="centered")
st.title("📄 KOC Contract Generator with ZIP Download")

uploaded_csv = st.file_uploader("Upload CSV File", type=["csv"])
uploaded_template = st.file_uploader("Upload Word Template (.docx)", type=["docx"])

if uploaded_csv and uploaded_template:
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
    st.download_button("📥 Download All Contracts (ZIP)", zip_buffer, file_name=f"KOC_Contracts_{today}.zip")
