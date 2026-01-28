from google import genai
import streamlit as st

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def generate_reply(prompt: str) -> str:
    try:
        # Try 'gemini-2.0-flash' first. 
        # If that fails, run the list_models script above to find your exact model name.
        response = client.models.generate_content(
    model="gemini-2.5-flash", # Try 'gemini-1.5-flash-001' if this fails
    contents=prompt
)

        if response.text:
            return response.text.strip()
        return "No response generated."

    except Exception as e:
        # This will print the full error to your Streamlit app to help debug
        return f"Error: {str(e)}"