import streamlit as st
from groq import Groq

# --- Page Setup ---
st.set_page_config(page_title="Aaru Cutie Assistant", page_icon="🎀", layout="centered")

# --- CSS for Background & Hearts ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #ff69b4; }
    @keyframes move { from { transform: translateY(100vh); opacity: 1; } to { transform: translateY(-10vh); opacity: 0; } }
    .heart { position: absolute; color: rgba(255, 105, 180, 0.3); font-size: 20px; animation: move 6s linear infinite; z-index: -1; }
    .main-title { text-align: center; color: #ff1493; font-size: 40px; text-shadow: 0 0 15px #ff1493; }
    .stChatMessage { background: rgba(255, 255, 255, 0.1) !important; border-radius: 15px; border: 1px solid #ff69b4; color: white !important; }
    </style>
    <div class="heart" style="left:15%; animation-delay:0s;">❤️</div>
    <div class="heart" style="left:45%; animation-delay:2s;">💖</div>
    <div class="heart" style="left:85%; animation-delay:4s;">💕</div>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>✨ AARU CUTIE ASSISTANT ✨</h1>", unsafe_allow_html=True)

# --- Voice Engine (JavaScript) ---
def aaru_voice_engine():
    js_code = """
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'hi-IN';
    recognition.continuous = false;
    
    function speak(text) {
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = 'hi-IN';
        window.speechSynthesis.speak(msg);
    }

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: transcript}, '*');
    };

    window.startAaru = () => { recognition.start(); };
    </script>
    <div style="text-align: center; margin-bottom: 10px;">
        <button onclick="startAaru()" style="background: #ff1493; color: white; border-radius: 25px; padding: 10px 25px; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 0 10px #ff1493;">
            🎙️ Tap & Speak (Cutie Aaru)
        </button>
    </div>
    """
    return st.components.v1.html(js_code, height=60)

# --- Brain Logic (Groq) ---
client = Groq(api_key="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")

# Inputs
voice_val = aaru_voice_engine()
chat_val = st.chat_input("Aaru se baatein karein...")

user_query = chat_val if chat_val else voice_val

if user_query and isinstance(user_query, str):
    # Display User Message
    with st.chat_message("user"):
        st.write(user_query)

    # Simple No-History Prompt for Speed & Stability
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Tum Aaru ho, ek cute flirty assistant. Har reply 'Ji Boss...' se shuru karo. Hinglish mein baat karo."},
                {"role": "user", "content": user_query}
            ]
        )
        reply = response.choices[0].message.content

        # Display & Speak Response
        with st.chat_message("assistant"):
            st.write(reply)
        
        st.components.v1.html(f"""
            <script>
            const msg = new SpeechSynthesisUtterance("{reply.replace('"', "'")}");
            msg.lang = 'hi-IN';
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)
    except Exception as e:
        st.error("Uff Boss! System busy hai, thodi der baad try karein.")
