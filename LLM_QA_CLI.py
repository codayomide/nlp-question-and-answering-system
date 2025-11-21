import os
import re
import google.generativeai as genai

# --- CONFIGURATION ---
# PASTE YOUR GEMINI API KEY HERE
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
  st.error("API Key is missing. Please set the GEMINI_API_KEY environment variable on Render.")
  st.stop()

# Configure the API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def basic_preprocessing(text):
    """
    1. Lowercase
    2. Remove punctuation
    3. Simple Tokenization
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    return tokens, " ".join(tokens)

def get_llm_response(processed_text):
    try:
        response = model.generate_content(processed_text)
        return response.text
    except Exception as e:
        return f"Error contacting API: {e}"

def main():
    print("--- CLI NLP Q&A System (Gemini Powered) ---")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter your question: ")
        
        if user_input.lower() == 'exit':
            break
            
        tokens, processed_text = basic_preprocessing(user_input)
        
        print(f"\n[DEBUG] Processed Query: {processed_text}")
        print("Fetching answer...")
        
        answer = get_llm_response(processed_text)
        
        print("\n--- Answer ---")
        print(answer)
        print("-" * 30 + "\n")

if __name__ == "__main__":
    main()