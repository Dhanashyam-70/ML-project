import streamlit as st
import joblib
from pathlib import Path

st.set_page_config(page_title="Inbox Guardian | SMS checker", page_icon="🛡️", layout="centered")

MODEL_PATH = Path(__file__).with_name("spam_model.joblib")
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

# Clean, responsive visual style
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
.stApp {background: radial-gradient(ellipse at 10% 0%, #e7f5ff 0, transparent 40%), linear-gradient(160deg,#f8fbff,#f4f7fb); color:#14253d;}
.block-container {max-width:850px; padding-top:2.2rem;}
.hero {background:linear-gradient(125deg,#102c4e,#174f71 62%,#18a6a0); color:white; padding:2.3rem 2.5rem; border-radius:24px; box-shadow:0 18px 45px #14375922; margin-bottom:1.5rem;}
.hero h1 {font-family:'Space Grotesk',sans-serif; font-size:2.6rem; margin:0 0 .5rem;}
.hero p {color:#d6e9f3; font-size:1.05rem; margin:.2rem 0;}
.eyebrow {text-transform:uppercase;letter-spacing:.16em;color:#75e0d0;font-size:.75rem;font-weight:800;}
.card {background:white;border:1px solid #e6edf4;border-radius:18px;padding:1.3rem 1.5rem;box-shadow:0 8px 24px #193a5a0b;}
.small {color:#62748a;font-size:.92rem;}
div.stButton > button {background:#118b83;color:white;border:0;border-radius:12px;padding:.65rem 1.3rem;font-weight:700;}
div.stButton > button:hover {background:#0b716c;color:white;border:0;}
textarea, input {pointer-events:auto !important; user-select:text !important; -webkit-user-select:text !important;}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='hero'><div class='eyebrow'>Machine Learning • SMS Safety</div><h1>Inbox Guardian</h1><p>Check a text message for common spam signals in seconds.</p></div>", unsafe_allow_html=True)

if not MODEL_PATH.exists():
    st.error("Model file not found. Download spam_model.joblib from Colab and place it beside app.py.")
    st.stop()
model = load_model()

st.markdown("### Check a message")
st.markdown("<p class='small'>Paste a message below. Your text is checked by the model trained in Google Colab.</p>", unsafe_allow_html=True)
with st.form("sms_check_form", clear_on_submit=False):
    message = st.text_area(
        "SMS message",
        placeholder="Type or paste a message here. Example: You have won an iPhone!",
        height=145,
        key="sms_message",
        disabled=False,
    )
    check = st.form_submit_button("Check message", use_container_width=True)
st.caption("Try: Are we still meeting at 5 today?")

if check:
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        # The model handles general language patterns; this tiny rule catches
        # common prize scams that may be too short for the model to recognize.
        normalized_message = " ".join(message.lower().split())
        prize_phrases = ("you have won", "you've won", "won an iphone", "win an iphone", "claim your prize", "free prize")
        matched_prize_phrase = any(phrase in normalized_message for phrase in prize_phrases)
        label = "spam" if matched_prize_phrase else model.predict([message])[0]
        st.divider()
        if label == "spam":
            st.error("🚨 Likely SPAM — be careful with links, requests, and unknown numbers.")
            if matched_prize_phrase:
                st.caption("Flagged by the prize-scam phrase check.")
        else:
            st.success("✅ Likely HAM — the model considers this a normal message.")
        st.caption("This is a classroom machine learning demo. Predictions can be wrong; never rely on it as a security guarantee.")

st.markdown("<br><div class='card'><b>How it works</b><br><span class='small'>TF-IDF converts message words into weighted numbers. A Linear SVM learns patterns that separate spam from normal messages.</span></div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#8291a3;font-size:.8rem;margin-top:1.8rem'>SMS Spam Detector • ML Lab Project</p>", unsafe_allow_html=True)
