import streamlit as st
from groq import Groq

# --- Page Setup ---
st.set_page_config(page_title="Aaru Cutie Assistant", page_icon="🎀", layout="centered")

# --- Full CSS: Animated Hearts, Background & Styles ---
st.markdown("""
    <style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ff69b4;
    }

    /* Floating Hearts Animation */
    @keyframes move {
        0% { transform: translateY(100vh) scale(0); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(-10vh) scale(1.2); opacity: 0; }
    }
    .heart {
        position: fixed;
        color: rgba(255, 105, 180, 0.6);
        font-size: 25px;
        animation: move 6s linear infinite;
        z-index: 0;
        pointer-events: none;
    }

    /* UI Components Styling */
    .main-title { text-align: center; color: #ff1493; font-size: 42px; text-shadow: 0 0 20px #ff1493; font-weight: bold; }
    .stChatMessage { background: rgba(255, 255, 255, 0.1) !important; border-radius: 15px; border: 1px solid #ff69b4; color: white !important; }
    .stChatInput textarea { color: white !important; }
    </style>

    <div class="heart" style="left:10%; animation-delay:0s;">❤️</div>
    <div class="heart" style="left:25%; animation-delay:2s;">💖</div>
    <div class="heart" style="left:45%; animation-delay:1s;">💗</div>
    <div class="heart" style="left:65%; animation-delay:3s;">💕</div>
    <div class="heart" style="left:85%; animation-delay:1.5s;">💘</div>
    """, unsafe_allow_html=True)

# --- Heading & Anime Girl GIF ---
st.markdown("<h1 class='main-title'>🎀 AARU CUTIE ASSISTANT 🎀</h1>", unsafe_allow_html=True)

cols = st.columns([1, 2, 1])
with cols[1]:
    # Cutie Anime Girl GIF (Live Link)
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3bmZ3JmVwPXYxX2ludGVybmFsX2dpZl9ieV9iYyZjdD1z/v6aOebdcl9nyfWCv7L/giphy.gif", use_container_width=True)

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
        msg.pitch = 1.2; // Thodi ladki wali pitch
        window.speechSynthesis.speak(msg);
    }

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: transcript}, '*');
    };

    window.startAaru = () => { recognition.start(); };
    </script>
    <div style="text-align: center; margin-bottom: 20px;">
        <button onclick="startAaru()" style="background: linear-gradient(45deg, #ff1493, #ff69b4); color: white; border-radius: 30px; padding: 12px 35px; border: none; cursor: pointer; font-size: 16px; font-weight: bold; box-shadow: 0 0 15px rgba(255, 20, 147, 0.6);">
            🎙️ Tap to Speak (Cutie Aaru)
        </button>
    </div>
    """
    return st.components.v1.html(js_code, height=80)

# --- Brain Logic (Groq) ---
# Yahan humne temperature aur prompt ko super flirty banaya hai
client = Groq(api_key="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")

voice_val = aaru_voice_engine()
chat_val = st.chat_input("Aaru se baatein karein ya button dabayein...")

# Logic to pick input
user_query = chat_val if chat_val else voice_val

if user_query and isinstance(user_query, str):
    with st.chat_message("user"):
        st.write(user_query)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "Tumhara naam Aaru hai. Tum ek bohot hi attractive, flirty aur playful assistant ho. Tum user ko 'Boss' ya 'Hero' bolti ho. Har reply 'Ji Boss...' se shuru karo aur bohot zyada flirting karo. Nakhre dikhao aur thoda shararti bano."
                },
                {"role": "user", "content": user_query}
            ],
            temperature=0.95 # Max creativity for flirting
        )
        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.write(reply)
        
        # Super Fast Voice Reply
        st.components.v1.html(f"""
            <script>
            const msg = new SpeechSynthesisUtterance("{reply.replace('"', "'")}");
            msg.lang = 'hi-IN';
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)
    except Exception as e:
        st.error("Uff Boss! Aaru sharma gayi, thodi der baad try karein.")
