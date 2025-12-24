import streamlit as st
import google.generativeai as genai

# Setup the Tool
st.set_page_config(page_title="AI Decision Extractor", layout="wide")
st.title("⚖️ AI Decision Extractor for Long Content")

# Sidebar for the API Key
with st.sidebar:
    api_key = st.text_input("Enter your Google API Key:", type="password")
    st.info("Get a free key at: aistudio.google.com")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("Upload Meeting Transcript or Document", type=['txt', 'pdf', 'md'])

    if uploaded_file and st.button("Extract Actionable Decisions"):
        # Read the file
        content = uploaded_file.read().decode("utf-8")
        
        with st.spinner('Scanning long content for decisions...'):
            prompt = f"Extract a table of decisions from this text. Include: Decision, Owner, and Deadline. Text: {content}"
            response = model.generate_content(prompt)
            st.success("Analysis Complete!")
            st.markdown(response.text)
else:
    st.warning("Please enter your API Key in the sidebar to start.")
