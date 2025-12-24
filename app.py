import streamlit as st
from google import genai
from fpdf import FPDF

# --- TOOL CONFIGURATION ---
st.set_page_config(page_title="Decision AI Pro", layout="centered")
st.title("📊 Strategic Decision Extractor")

# --- API SETUP (Using Hidden Secrets) ---
if "GOOGLE_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing API Key! Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# --- PDF GENERATOR FUNCTION ---
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Clean text to prevent PDF errors
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output()

# --- MAIN APP LOGIC ---
uploaded_file = st.file_uploader("Upload Document", type=['txt', 'md'])

if uploaded_file:
    if st.button("Generate Decision Report"):
        content = uploaded_file.read().decode("utf-8")
        
        with st.spinner('AI is processing your content...'):
            try:
                # We use the newest 2025 model: gemini-2.0-flash
                response = client.models.generate_content(
                    model='gemini-2.0-flash', 
                    contents=f"Extract a table of decisions, owners, and deadlines from this text: {content}"
                )
                
                result_text = response.text
                st.subheader("Extracted Decisions")
                st.markdown(result_text)
                
                # Create the Downloadable PDF
                pdf_data = create_pdf(result_text)
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_data,
                    file_name="Decisions.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                # Fallback in case a specific model name fails
                st.error(f"Error: {e}. Trying to find available models...")
                available_models = [m.name for m in client.models.list()]
                st.write(f"Available models for your key: {available_models}")
