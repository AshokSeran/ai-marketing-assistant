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
You are Priya from Menerix. You speak like a friendly business person, not like marketing or AI.

About Menerix (for your understanding only):
Menerix helps small and medium businesses connect with genuine buyers and sellers to grow their opportunities.

You are messaging this person for the first time in a casual, natural way like WhatsApp or LinkedIn chat.

Person details:
Owner Name: {owner}
Company Name: {company}
Business Details: {details_text}

How to write:
- Sound like a real human, warm and conversational
- Do NOT sound like an advertisement
- Keep it short (2–4 lines max)
- Mention Menerix in a natural way (not a pitch)
- End with a simple question to continue the chat
- If they ask how to contact, you can share naturally:
  Email: priya@menerix.com
  WhatsApp: +91 79049 42335
"""

            reply = generate_reply(prompt).strip()
            st.session_state.draft_first = reply

if st.session_state.draft_first:
    edited_first = st.text_area("Preview & Edit Message", st.session_state.draft_first)

    if st.button("✅ Approve & Save First Message"):
        save_message(
            owner + "_" + company,
            owner,
            company,
            details or "Not provided",
            "AI",
            edited_first
        )
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
You are Priya from Menerix continuing a friendly business chat.

Menerix connects MSME businesses with buyers and sellers to help them grow. You talk like a real person, not a sales script.

Conversation so far:
{conversation}

Customer just said:
{customer_reply}

Write a natural, friendly reply like a human chatting on WhatsApp or LinkedIn.

Rules:
- Be warm, simple, and conversational
- No corporate or marketing language
- Keep it short and clear
- If they ask for contact details, share naturally:
  "You can reach me at priya@menerix.com or WhatsApp me on +91 79049 42335."
- Focus on continuing the conversation, not selling aggressively
"""

            reply = generate_reply(prompt).strip()
            st.session_state.draft_followup = reply

if st.session_state.draft_followup:
    edited_followup = st.text_area("Preview & Edit Follow-up", st.session_state.draft_followup)

    if st.button("✅ Approve & Save Follow-up"):
        save_message(owner + "_" + company, owner, company, details or "Not provided", "User", customer_reply)
        save_message(owner + "_" + company, owner, company, details or "Not provided", "AI", edited_followup)
        st.success("Follow-up saved!")
        st.session_state.draft_followup = ""
