import json
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)
sheet = client.open("AI_Marketing_Chat").sheet1

def save_message(user_id, owner, company, details, role, message):
    sheet.append_row([
        user_id,
        owner,
        company,
        details,
        role,
        message,
        str(datetime.now())
    ])

def get_last_messages(user_id, limit=6):
    rows = sheet.get_all_records()
    user_msgs = [r for r in rows if r["user_id"] == user_id]
    return user_msgs[-limit:]
