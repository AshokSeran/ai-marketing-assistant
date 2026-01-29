import streamlit as st
from google import genai
from google.genai import errors

# Initialize the new SDK Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def generate_reply(prompt: str) -> str:
    try:
        # Use the specific Flash-Lite model for maximum free-tier limits
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=prompt
        )
        return response.text

    except errors.ClientError as e:
        # Check for the specific 'Limit: 0' or 'Quota' error
        if "quota" in str(e).lower():
            return (
                "⚠️ Free Tier Quota Reached or Project not activated. "
                "Go to [Google AI Studio](https://aistudio.google.com) "
                "to check your API key status."
            )
        return f"❌ API Error: {e.message}"

    except Exception as e:
        return f"❌ System Error: {str(e)}"
