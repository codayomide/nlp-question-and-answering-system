import os
import streamlit as st
import re
import google.generativeai as genai

# --- CONFIGURATION ---
# For local testing, paste key here. For deployment, use st.secrets.
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- HELPER FUNCTIONS ---
def basic_preprocessing(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    return tokens, " ".join(tokens)

def get_llm_response(processed_text):
    try:
        response = model.generate_content(processed_text)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- STREAMLIT UI ---
st.set_page_config(page_title="NLP Q&A System", page_icon="⚡")

st.title("⚡ NLP Q&A System")
st.subheader("Powered by Google Gemini")

user_question = st.text_input("Enter your question here:")

if st.button("Get Answer"):
    if user_question:
        with st.spinner("Consulting Gemini..."):
            # 1. Preprocess
            tokens, processed_text = basic_preprocessing(user_question)
            
            # 2. Get Response
            answer = get_llm_response(processed_text)
            
            # 3. Display
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("Processed Question")
                st.write(processed_text)
                st.caption(f"Tokens: {tokens}")
            
            with col2:
                st.success("Gemini Answer")
                st.write(answer)
    else:
        st.warning("Please enter a question first.")

st.markdown("---")
st.text("Submitted by: [Your Name] | [Matric Number]")