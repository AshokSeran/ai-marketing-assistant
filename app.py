import streamlit as st
from services.gemini_service import generate_reply
from services.sheets_service import save_message, get_last_messages

st.set_page_config(page_title="AI Marketing Assistant", layout="centered")
st.title("🤖 AI Marketing Assistant")

# ---------------- USER INPUTS ----------------
user_id = st.text_input("Customer ID (Phone or Email)")
owner = st.text_input("Owner Name")
company = st.text_input("Company Name")
details = st.text_area("Business Details")

# ---------------- SESSION STATE ----------------
if "draft_first" not in st.session_state:
    st.session_state.draft_first = ""

if "draft_followup" not in st.session_state:
    st.session_state.draft_followup = ""

# =========================================================
# 📤 FIRST MESSAGE
# =========================================================
st.header("📤 First Outreach Message")

if st.button("Generate First Message", key="gen_first"):
    if not owner or not company or not details:
        st.warning("Please fill Owner, Company, and Business Details")
    else:
        with st.spinner("Generating message..."):
            prompt = f"""
            Write a friendly marketing message.

            Owner: {owner}
            Company: {company}
            Business Details: {details}
            """
            st.session_state.draft_first = generate_reply(prompt)

if st.session_state.draft_first:
    edited_first = st.text_area(
        "Preview First Message",
        st.session_state.draft_first,
        key="edit_first"
    )

    if st.button("Approve & Save First Message", key="save_first"):
        save_message(user_id, owner, company, details, "AI", edited_first)
        st.success("First message saved!")
        st.session_state.draft_first = ""

# =========================================================
# 💬 FOLLOW-UP MESSAGE
# =========================================================
st.header("💬 Follow-up Reply")

customer_reply = st.text_area("Customer Reply", key="cust_reply")

if st.button("Generate Follow-up Reply", key="gen_follow"):
    if not user_id or not customer_reply:
        st.warning("Customer ID and reply are required")
    else:
        with st.spinner("Thinking of the best reply..."):
            history = get_last_messages(user_id)

            conversation = "\n".join([
                f"{h.get('role','User')}: {h.get('message','')}"
                for h in history
            ])

            prompt = f"""
            Continue this marketing conversation naturally and persuasively.

            Conversation so far:
            {conversation}

            Customer just said:
            {customer_reply}
            """

            st.session_state.draft_followup = generate_reply(prompt)

if st.session_state.draft_followup:
    edited_followup = st.text_area(
        "Preview Follow-up",
        st.session_state.draft_followup,
        key="edit_follow"
    )

    if st.button("Approve & Save Follow-up", key="save_follow"):
        save_message(user_id, owner, company, details, "User", customer_reply)
        save_message(user_id, owner, company, details, "AI", edited_followup)
        st.success("Follow-up saved!")
        st.session_state.draft_followup = ""
