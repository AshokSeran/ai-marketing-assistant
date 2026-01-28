import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

def generate_reply(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()
