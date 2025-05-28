import streamlit as st
from docxtpl import DocxTemplate
from datetime import date
import io

st.set_page_config(page_title="KOC Contract Generator", layout="centered", page_icon="📝")
st.title("📝 KOC Contract Generator")

mode = st.radio("Choose Input Mode", ["Manual Entry for Single Contract"])

uploaded_template = st.file_uploader("📄 Upload Word Template (.docx)", type=["docx"])

if mode == "Manual Entry for Single Contract":
    st.subheader("🧾 Fill in Influencer Contract Details")

    if uploaded_template:
        with st.form("manual_contract_form"):
            Influencer_name = st.text_input("Influencer Name")
            Influencer_email = st.text_input("Influencer Email")
            Influencer_contact = st.text_input("Influencer Contact")
            Influencer_address = st.text_input("Influencer Address")
            platform = st.selectbox("Platform", ["TikTok", "Instagram", "YouTube", "Facebook", "Other"])
            platform_username = st.text_input("Platform Username")
            Influencer_links = st.text_area("Influencer Links (separate with commas)")
            promotion_date = st.date_input("Promotion Date", value=date.today())
            video_rate = st.number_input("Video Rate (USD)", min_value=0.0, step=1.0)
            bonus_info = st.text_area("Bonus Info")
            payment_method = st.selectbox("Payment Method", ["PayPal", "Bank Transfer", "GCash", "Others"])
            payment_information = st.text_area("Payment Information")
            payment_charges = st.number_input("Payment Charges (USD)", min_value=0.0, step=1.0)

            submitted = st.form_submit_button("📄 Generate Contract")

        if submitted:
            try:
                template = DocxTemplate(uploaded_template)

                context = {
                    'Influencer_name': Influencer_name,
                    'Influencer_email': Influencer_email,
                    'Influencer_contact': Influencer_contact,
                    'Influencer_address': Influencer_address,
                    'platform': platform,
                    'platform_username': platform_username,
                    'Influencer_links': Influencer_links,
                    'promotion_date': promotion_date.strftime("%Y-%m-%d"),
                    'video_rate': video_rate,
                    'bonus_info': bonus_info,
                    'payment_method': payment_method,
                    'payment_information': payment_information,
                    'payment_charges': payment_charges
                }

                template.render(context)

                output = io.BytesIO()
                template.save(output)
                output.seek(0)

                st.success("✅ Contract generated successfully!")
                st.download_button(
                    label="📥 Download Contract",
                    data=output,
                    file_name=f"KOC_Contract_{Influencer_name.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"❌ Error generating contract: {e}")
    else:
        st.info("⬆️ Please upload a Word DOCX template to continue.")
