import streamlit as st
import time
from google import genai
from google.genai import errors

# Initialize client using secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def generate_reply(prompt: str) -> str:
    # 2.0 Flash-Lite is optimized for speed and cost
    MODEL_ID = "gemini-2.0-flash-lite" 
    retries = 4
    base_delay = 2 

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt
            )

            # Access .text directly for simplicity; returns the concatenated response
            if response.text:
                return response.text
            return "No response content found."

        # 🛑 Handle 429 (Rate Limit) and 503 (Overloaded)
        except (errors.ServerError, errors.ClientError) as e:
            error_msg = str(e).lower()
            if "503" in error_msg or "429" in error_msg or "overloaded" in error_msg:
                if attempt < retries - 1:
                    wait_time = base_delay * (2 ** attempt)  # 2s, 4s, 8s...
                    st.warning(f"Server busy. Retrying in {wait_time}s... (Attempt {attempt + 1})")
                    time.sleep(wait_time)
                    continue
            
            # Catch blocked content or invalid requests
            st.error(f"Gemini API Error: {e}")
            return f"Error: {e}"

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            break

    return "Failed to get a response after multiple attempts."

# Simple Streamlit usage
user_input = st.text_input("Ask Gemini 2.0 Flash-Lite:")
if user_input:
    with st.spinner("Thinking..."):
        answer = generate_reply(user_input)
        st.write(answer)
