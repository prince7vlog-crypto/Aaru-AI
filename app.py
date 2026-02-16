import streamlit as st
from groq import Groq

# --- Page Setup ---
st.set_page_config(page_title="Aaru Cutie Assistant", page_icon="🎀", layout="centered")

# --- CSS for Animated Background ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #ff69b4; }
    @keyframes move { from { transform: translateY(100vh); opacity: 1; } to { transform: translateY(-10vh); opacity: 0; } }
    .heart { position: absolute; color: rgba(255, 105, 180, 0.4); font-size: 20px; animation: move 5s linear infinite; z-index: -1; }
    .main-title { text-align: center; color: #ff1493; font-size: 45px; text-shadow: 0 0 15px #ff1493; }
    .instruction-box { background: rgba(255, 105, 180, 0.1); border: 2px solid #ff69b4; padding: 15px; border-radius: 20px; text-align: center; backdrop-filter: blur(5px); }
    .stChatMessage { background: rgba(255, 255, 255, 0.1) !important; border-radius: 15px; border: 1px solid #ff69b4; color: white !important; }
    </style>
    <div class="heart" style="left:10%; animation-delay:0s;">❤️</div>
    <div class="heart" style="left:50%; animation-delay:1s;">💗</div>
    <div class="heart" style="left:80%; animation-delay:3s;">💕</div>
    """, unsafe_allow_html=True)

# --- Memory Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h1 class='main-title'>✨ AARU CUTIE ASSISTANT ✨</h1>", unsafe_allow_html=True)

cols = st.columns([1, 2, 1])
with cols[1]:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3JmVwPXYxX2ludGVybmFsX2dpZl9ieV9iYyZjdD1z/v6aOebdcl9nyfWCv7L/giphy.gif", use_container_width=True)

# --- Voice Engine ---
def aaru_engine():
    js_code = """
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'hi-IN';
    recognition.continuous = true;
    function speak(text) {
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = 'hi-IN';
        window.speechSynthesis.speak(msg);
    }
    recognition.onresult = (event) => {
        const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase();
        if (transcript.includes("cutie aaru") || transcript.includes("kyuti aaru")) {
            const command = transcript.replace(/cutie aaru|kyuti aaru/g, "").trim();
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: command}, '*');
        }
    };
    window.startAaru = () => { recognition.start(); speak("Ji Boss, Cutie Aaru sun rahi hai!"); };
    </script>
    <div style="text-align: center; margin-top: 20px;">
        <button onclick="startAaru()" style="background: linear-gradient(45deg, #ff1493, #ff69b4); color: white; border-radius: 30px; padding: 12px 35px; border: none; cursor: pointer; font-weight: bold;">
            🎙️ Activate Cutie Aaru
        </button>
    </div>
    """
    return st.components.v1.html(js_code, height=100)

# --- Process Command ---
client = Groq(api_key="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")
user_command = aaru_engine()

if user_command:
    # Update Memory
    st.session_state.messages.append({"role": "user", "content": user_command})
    
    # System Prompt
    sys_prompt = {"role": "system", "content": "Tum Aaru ho, ek cute flirty assistant. User ka naam yaad rakho. Hinglish mein baat karo."}
    
    # Create combined message list for Groq
    full_chat_history = [sys_prompt] + st.session_state.messages

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_chat_history
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.write(reply)
        
        # Voice Output
        st.components.v1.html(f"""
            <script>
            const msg = new SpeechSynthesisUtterance("{reply.replace('"', "'")}");
            msg.lang = 'hi-IN';
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)
    except Exception as e:
        st.error(f"Uff! Error: {e}")
        
