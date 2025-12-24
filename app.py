import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Function to create the PDF
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    return pdf.output(dest='S').encode('latin-1')

st.set_page_config(page_title="AI Decision Extractor", layout="wide")
st.title("⚖️ AI Decision Extractor for Long Content")

with st.sidebar:
    api_key = st.text_input("Enter your Google API Key:", type="password")
    st.info("Get a free key at: aistudio.google.com")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("Upload Meeting Transcript or Document", type=['txt', 'md'])

    if uploaded_file and st.button("Extract Actionable Decisions"):
        content = uploaded_file.read().decode("utf-8")
        
        with st.spinner('Scanning content...'):
            prompt = f"Extract a clear list of decisions, owners, and deadlines from this text: {content}"
            response = model.generate_content(prompt)
            result_text = response.text
            
            st.success("Analysis Complete!")
            st.markdown(result_text)
            
            # The Download Button
            pdf_data = create_pdf(result_text)
            st.download_button(
                label="Download Report as PDF",
                data=pdf_data,
                file_name="Decision_Report.pdf",
                mime="application/pdf"
            )
else:
    st.warning("Please enter your API Key in the sidebar.")
