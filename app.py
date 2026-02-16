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
    .stChatMessage { background: rgba(255, 255, 255, 0.1) !important; border-radius: 15px; border: 1px solid #ff69b4; color: white !important; }
    /* Chat input color fix */
    .stChatInput textarea { color: white !important; }
    </style>
    <div class="heart" style="left:10%; animation-delay:0s;">❤️</div>
    <div class="heart" style="left:50%; animation-delay:1s;">💗</div>
    """, unsafe_allow_html=True)

# --- Memory Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<h1 class='main-title'>✨ AARU CUTIE ASSISTANT ✨</h1>", unsafe_allow_html=True)

# --- Voice Engine (JavaScript) ---
def aaru_voice_engine():
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

    window.startAaru = () => { 
        recognition.start(); 
        speak("Ji Boss, Cutie Aaru ab sun rahi hai!"); 
    };
    </script>
    <div style="text-align: center; margin-bottom: 20px;">
        <button onclick="startAaru()" style="background: linear-gradient(45deg, #ff1493, #ff69b4); color: white; border-radius: 30px; padding: 12px 35px; border: none; cursor: pointer; font-weight: bold; box-shadow: 0 0 15px #ff1493;">
            🎙️ Activate Voice (Cutie Aaru)
        </button>
    </div>
    """
    return st.components.v1.html(js_code, height=100)

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Brain (Groq Logic) ---
client = Groq(api_key="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")

def get_aaru_response(user_text):
    st.session_state.messages.append({"role": "user", "content": user_text})
    sys_prompt = {"role": "system", "content": "Tum Aaru ho, ek cute flirty assistant. User ka naam yaad rakho. Har reply 'Ji Boss...' se shuru karo."}
    full_history = [sys_prompt] + st.session_state.messages
    
    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=full_history)
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    return reply

# --- Inputs: Voice or Chat ---
voice_command = aaru_voice_engine()
chat_input = st.chat_input("Aaru ko kuch likho ya voice activate karo...")

final_query = None
if voice_command:
    final_query = voice_command
elif chat_input:
    final_query = chat_input

# --- Execute Response ---
if final_query:
    if not chat_input: # Agar voice se aaya toh user message dikhao
        with st.chat_message("user"):
            st.write(final_query)
            
    reply_text = get_aaru_response(final_query)
    
    with st.chat_message("assistant"):
        st.write(reply_text)
    
    # Fast Voice Reply
    st.components.v1.html(f"""
        <script>
        const msg = new SpeechSynthesisUtterance("{reply_text.replace('"', "'")}");
        msg.lang = 'hi-IN';
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)
