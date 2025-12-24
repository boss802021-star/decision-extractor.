import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# 1. Secret Configuration - This pulls the key from your hidden settings
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key missing! Please add it to the Streamlit Secrets.")

# Function to create the PDF
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Clean text for PDF encoding
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output(dest='S')

st.set_page_config(page_title="Decision AI Pro", layout="centered")
st.title("📊 Strategic Decision Extractor")
st.markdown("Upload your content below. Our AI will identify key decisions, owners, and deadlines.")

# Using 'gemini-1.5-flash' which is the most stable free-tier model
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Upload Document (Text or Markdown)", type=['txt', 'md'])

if uploaded_file:
    if st.button("Generate Decision Report"):
        content = uploaded_file.read().decode("utf-8")
        
        with st.spinner('Analyzing content...'):
            prompt = f"""
            You are an expert project manager. Extract every decision from the text below.
            Format it as a table with columns: Decision, Assigned To, and Deadline.
            If no deadline is found, write 'N/A'.
            
            Text: {content}
            """
            try:
                response = model.generate_content(prompt)
                result_text = response.text
                
                st.subheader("Extracted Decisions")
                st.markdown(result_text)
                
                # PDF Download
                pdf_data = create_pdf(result_text)
                st.download_button(
                    label="📥 Download Professional PDF Report",
                    data=pdf_data,
                    file_name="Decision_Report.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"AI Error: {e}")
