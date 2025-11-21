import os
import re
# You need to install the groq library: pip install groq
from groq import Groq

# --- CONFIGURATION ---
# PASTE YOUR API KEY HERE IF NOT SET IN ENVIRONMENT VARIABLES
API_KEY = "PASTE_YOUR_GROQ_API_KEY_HERE" 

client = Groq(api_key=API_KEY)

def basic_preprocessing(text):
    """
    1. Lowercase
    2. Remove punctuation
    3. Simple Tokenization (splitting by space)
    """
    # Lowercase
    text = text.lower()
    # Remove punctuation using regex
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize
    tokens = text.split()
    # Return both the list of tokens and the reconstructed string
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
            model="llama3-8b-8192", # Free and fast model on Groq
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error contacting API: {e}"

def main():
    print("--- CLI NLP Q&A System ---")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter your question: ")
        
        if user_input.lower() == 'exit':
            break
            
        # Preprocess
        tokens, processed_text = basic_preprocessing(user_input)
        
        print(f"\n[DEBUG] Processed/Cleaned Query: {processed_text}")
        print("Fetching answer...")
        
        # Get Answer
        answer = get_llm_response(processed_text)
        
        print("\n--- Answer ---")
        print(answer)
        print("-" * 30 + "\n")

if __name__ == "__main__":
    main()