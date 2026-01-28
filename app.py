import streamlit as st
from services.gemini_service import generate_reply
from services.sheets_service import save_message, get_last_messages

st.set_page_config(page_title="Menerix AI Assistant", layout="centered")
st.title("🤖 Menerix AI Business Connect Assistant")

# ---------------- USER INPUTS ----------------
owner = st.text_input("Owner Name *")
company = st.text_input("Company Name *")
details = st.text_area("Business Details (Optional)")

# ---------------- SESSION STATE ----------------
if "draft_first" not in st.session_state:
    st.session_state.draft_first = ""

if "draft_followup" not in st.session_state:
    st.session_state.draft_followup = ""

# =========================================================
# 📤 FIRST OUTREACH MESSAGE
# =========================================================
st.header("📤 First Outreach Message")

if st.button("Generate First Message"):
    if not owner or not company:
        st.warning("Owner Name and Company Name are required")
    else:
        with st.spinner("Writing a natural message..."):

            details_text = details if details else "Not provided"

            prompt = f"""
You are Tamil Inaiyan, a real person from a company called Menerix.

Menerix is an MSME-focused platform that connects sellers with buyers and helps businesses find new opportunities.

Write a short, friendly, natural message like a real person sending a WhatsApp or LinkedIn message.

Customer:
Owner Name: {owner}
Company Name: {company}
Business Details: {details_text}

Guidelines:
- Use simple, natural English
- Sound like a real person, not marketing
- Keep it 2–4 short lines
- Mention that Menerix helps businesses connect with buyers/sellers
- End with a casual question
"""

            st.session_state.draft_first = generate_reply(prompt)

if st.session_state.draft_first:
    edited_first = st.text_area("Preview & Edit Message", st.session_state.draft_first)

    if st.button("✅ Approve & Save First Message"):
        save_message(owner + "_" + company, owner, company, details or "Not provided", "AI", edited_first)
        st.success("First message saved!")
        st.session_state.draft_first = ""

# =========================================================
# 💬 FOLLOW-UP REPLY
# =========================================================
st.header("💬 Follow-up Reply")

customer_reply = st.text_area("Customer Reply")

if st.button("Generate Follow-up Reply"):
    if not owner or not company or not customer_reply:
        st.warning("Owner Name, Company Name and reply are required")
    else:
        with st.spinner("Writing a friendly reply..."):
            history = get_last_messages(owner, company)

            conversation = "\n".join([
                f"{h.get('role','User')}: {h.get('message','')}"
                for h in history
            ])

            prompt = f"""
You are Tamil Inaiyan from Menerix, continuing a casual business chat.

Menerix connects sellers with buyers and helps MSMEs find new business opportunities.

Conversation so far:
{conversation}

Customer just said:
{customer_reply}

Reply naturally like a real human in a business chat.
Keep it short, friendly, and simple.
"""

            st.session_state.draft_followup = generate_reply(prompt)

if st.session_state.draft_followup:
    edited_followup = st.text_area("Preview & Edit Follow-up", st.session_state.draft_followup)

    if st.button("✅ Approve & Save Follow-up"):
        save_message(owner + "_" + company, owner, company, details or "Not provided", "User", customer_reply)
        save_message(owner + "_" + company, owner, company, details or "Not provided", "AI", edited_followup)
        st.success("Follow-up saved!")
        st.session_state.draft_followup = ""
