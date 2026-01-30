import streamlit as st
import time
from google import genai
from google.genai import errors

# Initialize client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


def generate_reply(prompt: str) -> str:
    retries = 4

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview"  # fallback: gemini-1.5-flash
                contents=prompt
            )

            # Safe way to extract text
            return response.candidates[0].content.parts[0].text

        # 🔁 Handle temporary overload (503)
        except errors.ServerError as e:
            if "503" in str(e) or "overloaded" in str(e).lower():
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            return "⚠️ Server error. Please try again later."

        # 💳 Handle quota / billing issues
        except errors.ClientError as e:
            if "quota" in str(e).lower():
                return "⚠️ Free tier quota reached or billing not enabled."
            return f"Client error: {str(e)}"

        except Exception as e:
            return f"Unexpected error: {str(e)}"

    return "⚠️ AI server is busy. Please try again in a moment."