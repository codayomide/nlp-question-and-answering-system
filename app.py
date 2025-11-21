import streamlit as st
import re
import os
from groq import Groq

# --- CONFIGURATION ---
# Ideally, load this from st.secrets in production, 
# but for this specific assignment submission, you can paste it or use env vars.
API_KEY = "PASTE_YOUR_GROQ_API_KEY_HERE" 

# Initialize Client
client = Groq(api_key=API_KEY)

# --- HELPER FUNCTIONS ---
def basic_preprocessing(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize
    tokens = text.split()
    return tokens, " ".join(tokens)

def get_llm_response(processed_text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": processed_text,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- STREAMLIT UI ---
st.set_page_config(page_title="NLP Q&A System", page_icon="🤖")

st.title("🤖 NLP Q&A System")
st.subheader("Project 2 - LLM API Integration")

# User Input
user_question = st.text_input("Enter your question here:")

if st.button("Get Answer"):
    if user_question:
        with st.spinner("Processing and thinking..."):
            # 1. Preprocess
            tokens, processed_text = basic_preprocessing(user_question)
            
            # 2. Get Response
            answer = get_llm_response(processed_text)
            
            # 3. Display Results
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("Processed Question (Cleaned)")
                st.write(processed_text)
                st.caption(f"Tokens: {tokens}")
            
            with col2:
                st.success("LLM Answer")
                st.write(answer)
    else:
        st.warning("Please enter a question first.")

# Footer
st.markdown("---")
st.text("Submitted by: [Your Name] | [Matric Number]")