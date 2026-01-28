from google import genai
import streamlit as st

# Initialize client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def generate_reply(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text if response.text else "No response generated."

    except Exception as e:
        return f"Error generating response: {e}"
