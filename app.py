import streamlit as st
import requests

# ========== CONFIGURATION ==========
BACKEND_URL = "https://tailortalk-backend-2.onrender.com/chat"

# ========== PAGE SETUP ==========
st.set_page_config(
    page_title="TailorTalk - AI Chat for Appointments",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== CUSTOM CSS ==========
st.markdown("""
    <style>
    body {
        background-color: #101728;
        color: white;
    }
    .main {
        background-color: #101728;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #1e1e2f;
        color: #fff;
        border: 1px solid #555;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 12px;
        margin: 10px 0;
        max-width: 90%;
        line-height: 1.5;
    }
    .user {
        background-color: #2a2d45;
        text-align: right;
        margin-left: auto;
    }
    .bot {
        background-color: #214e4e;
        text-align: left;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ========== TITLE ==========
st.markdown("## 🧵 TailorTalk - Book Appointments with AI")
st.markdown("Ask anything related to booking your tailor appointment or queries!")

# ========== SLOT CHECKER ==========
with st.expander("📅 Check availability directly"):
    st.markdown("### Want to see all free slots for a date?")
    day = st.selectbox("Choose date expression", [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ])

    hardcoded_slots = {
        "Monday": ["12:30 PM - 3:00 PM", "5:00 PM - 7:00 PM"],
        "Tuesday": ["11:00 AM - 1:00 PM", "3:00 PM - 6:00 PM"],
        "Wednesday": ["10:30 AM - 12:30 PM", "4:00 PM - 6:30 PM"],
        "Thursday": ["1:00 PM - 3:30 PM", "6:00 PM - 8:00 PM"],
        "Friday": ["10:00 AM - 2:00 PM", "4:30 PM - 6:30 PM"],
        "Saturday": ["9:00 AM - 11:30 AM", "2:00 PM - 5:00 PM"],
        "Sunday": ["Closed"]
    }

    if st.button("🔍 Show Available Slots"):
        slots = hardcoded_slots.get(day, [])
        if slots:
            if slots == ["Closed"]:
                st.warning(f"❌ No slots available on {day}.")
            else:
                st.success(f"Available slots for **{day}**:")
                for s in slots:
                    st.markdown(f"• {s}")
        else:
            st.error("Something went wrong fetching slots.")

# ========== CHAT UI ==========
user_query = st.text_input("💬 Enter your message:", "")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Send"):
    if user_query.strip() == "":
        st.warning("Please enter a query.")
    else:
        st.session_state.chat_history.append(("user", user_query))
        try:
            response = requests.post(BACKEND_URL, json={"query": user_query})
            if response.status_code == 200:
                ai_reply = response.json().get("response", "No response")
                st.session_state.chat_history.append(("bot", ai_reply))
            else:
                st.session_state.chat_history.append(("bot", f"Error {response.status_code}: {response.text}"))
        except Exception as e:
            st.session_state.chat_history.append(("bot", f"Request failed: {e}"))

# ========== CHAT HISTORY ==========
st.markdown("---")
for role, message in st.session_state.chat_history:
    css_class = "user" if role == "user" else "bot"
    st.markdown(f"<div class='chat-bubble {css_class}'>{message}</div>", unsafe_allow_html=True)
