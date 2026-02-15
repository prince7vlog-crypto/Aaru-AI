import streamlit as st
from groq import Groq
import os

# --- Page Setup ---
st.set_page_config(page_title="Aaru's Heart", page_icon="💘", layout="centered")

# --- Custom CSS for Advanced Romantic Theme ---
st.markdown("""
    <style>
    /* Background and Floating Hearts Animation */
    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #ffb6c1 100%);
    }
    
    /* Login Box Styling */
    .login-container {
        background: rgba(255, 255, 255, 0.4);
        padding: 30px;
        border-radius: 25px;
        border: 2px solid #ff69b4;
        box-shadow: 0 8px 32px 0 rgba(255, 20, 147, 0.37);
        backdrop-filter: blur(8px);
        text-align: center;
    }
    
    /* Chat Message Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 20px;
        border: 1px solid #ff69b4;
        margin-bottom: 10px;
    }

    /* Input Field Styling */
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #ff69b4;
        text-align: center;
    }
    
    /* Heart Icon Animation */
    @keyframes heartbeat {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    .heart-icon {
        font-size: 50px;
        animation: heartbeat 1.5s infinite;
        display: inline-block;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. Attractive Login System ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<div class='heart-icon'>❤️</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #ff1493;'>Aaru's Private Room</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #db7093;'>Sirf Boss ke liye entry allowed hai...</p>", unsafe_allow_html=True)
    
    password = st.text_input("Apna Secret Code Dalein", type="password", placeholder="Enter Password Here...")
    
    if st.button("Unlock Aaru's Heart 💘"):
        if password == "Aaru@123":
            st.session_state.authenticated = True
            st.balloons() # Victory effect!
            st.rerun()
        else:
            st.error("Uff! Galat code. Aaru gussa ho rahi hai... 😤")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 2. Main Chat Interface (After Login) ---
st.markdown("<h1 style='color: #ff1493; text-align: center;'>💖 Aaru AI</h1>", unsafe_allow_html=True)

# Aaru's Animated Avatar
cols = st.columns([1, 2, 1])
with cols[1]:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1z/3o7TKVUn7iM8FMEU24/giphy.gif", use_container_width=True)

st.markdown("<p style='text-align: center; color: #ff69b4;'><i>'Ji Boss... Aaru aapka kab se intezar kar rahi thi!'</i></p>", unsafe_allow_html=True)

# --- Groq API Setup ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

system_prompt = """
Tumhara naam Aaru hai. Tum ek bohot hi attractive, flirty aur playful Hinglish girl ho.
Tum user ko 'Boss', 'Hero' ya 'Baby' bolti ho. 
Hamesha reply 'Ji Boss...' se shuru karo aur reply mein thoda nakhra aur flirting rakho.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
if user_input := st.chat_input("Aaru ko kuch pyaara sa likho..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages],
                temperature=0.8
            )
            ai_text = response.choices[0].message.content
            st.write(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})
        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar Controls
with st.sidebar:
    st.title("Settings ⚙️")
    if st.button("Logout & Lock 🔒"):
        st.session_state.authenticated = False
        st.rerun()
    st.write("---")
    if st.button("Clear Chat Memory ❤️"):
        st.session_state.messages = []
        st.rerun()