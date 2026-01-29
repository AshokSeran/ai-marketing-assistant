import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials
creds_dict = dict(st.secrets["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(creds)

# Open sheet safely
try:
    sheet = client.open("AI_Marketing_Chat").sheet1
except Exception as e:
    st.error(f"Google Sheet connection failed: {e}")
    sheet = None


def save_message(user_id, owner, company, details, role, message):
    """Append a chat message row to Google Sheets"""
    if not sheet:
        return

    try:
        sheet.append_row([
            str(user_id),
            owner,
            company,
            details,
            role,
            message,
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        ])
    except Exception as e:
        st.warning(f"Failed to save chat message: {e}")


def get_last_messages(user_id, limit=6):
    """Fetch last N messages for a specific user efficiently"""
    if not sheet:
        return []

    try:
        # Get all values (faster than get_all_records for big sheets)
        rows = sheet.get_all_values()

        if len(rows) < 2:
            return []

        headers = rows[0]
        data_rows = rows[1:]

        # Map column index safely
        header_map = {h: i for i, h in enumerate(headers)}

        if "user_id" not in header_map:
            st.error("Column 'user_id' not found in sheet")
            return []

        uid_index = header_map["user_id"]

        user_msgs = [
            dict(zip(headers, row))
            for row in data_rows
            if len(row) > uid_index and row[uid_index] == str(user_id)
        ]

        return user_msgs[int(-limit):]

    except Exception as e:
        st.warning(f"Failed to fetch messages: {e}")
        return []
