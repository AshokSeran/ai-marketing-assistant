import streamlit as st
from services.gemini_service import generate_reply
from services.sheets_service import save_message, get_last_messages

st.set_page_config(page_title="AI Marketing Assistant", layout="centered")

st.title("🤖 AI Marketing Assistant")

user_id = st.text_input("Customer ID (Phone or Email)")
owner = st.text_input("Owner Name")
company = st.text_input("Company Name")
details = st.text_area("Business Details")

if "draft_first" not in st.session_state:
    st.session_state.draft_first = ""

if "draft_followup" not in st.session_state:
    st.session_state.draft_followup = ""

# First Message
st.header("📤 First Outreach Message")

if st.button("Generate First Message"):
    prompt = f"""
    Write a friendly marketing message.

    Owner: {owner}
    Company: {company}
    Business Details: {details}
    """
    st.session_state.draft_first = generate_reply(prompt)

if st.session_state.draft_first:
    edited_first = st.text_area("Preview First Message", st.session_state.draft_first)

    if st.button("Approve & Save First Message"):
        save_message(user_id, owner, company, details, "AI", edited_first)
        st.success("Saved!")
        st.session_state.draft_first = ""

# Follow-up
st.header("💬 Follow-up Reply")

customer_reply = st.text_area("Customer Reply")

if st.button("Generate Follow-up Reply"):
    history = get_last_messages(user_id)
    conversation = "\n".join([f"{h['role']}: {h['message']}" for h in history])

    prompt = f"""
    Continue this marketing conversation.

    Conversation:
    {conversation}

    Customer said:
    {customer_reply}
    """
    st.session_state.draft_followup = generate_reply(prompt)

if st.session_state.draft_followup:
    edited_followup = st.text_area("Preview Follow-up", st.session_state.draft_followup)

    if st.button("Approve & Save Follow-up"):
        save_message(user_id, owner, company, details, "User", customer_reply)
        save_message(user_id, owner, company, details, "AI", edited_followup)
        st.success("Follow-up saved!")
        st.session_state.draft_followup = ""
