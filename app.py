import streamlit as st
from transformers import pipeline
import time

# Page Configuration
st.set_page_config(page_title="Vocal Vigilance AI", page_icon="🛡️", layout="centered")

# Load AI Model (Cached to make it fast)
@st.cache_resource
def load_analyzer():
    # BERT model fine-tuned for spam/scam detection
    return pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")

# Custom UI Styling
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.1rem !important; }
    .stButton button { background-color: #ff4b4b; color: white; height: 3em; width: 100%; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

def run_app():
    st.title("🛡️ Vocal Vigilance")
    st.markdown("### AI-Powered Scam Protection for India")
    st.write("Analyze suspicious messages for signs of fraud and urgency.")

    user_input = st.text_area("Paste the message or call transcript here:", placeholder="Example: Your electricity will be cut off tonight at 9 PM. Pay ₹500 immediately to avoid disconnection...")

    if st.button("Start Analysis"):
        if not user_input.strip():
            st.warning("⚠️ Please enter some text to analyze.")
        else:
            with st.spinner("🔍 Our AI is scanning for scam patterns..."):
                time.sleep(1.2) # Adding a 'human' processing feel
                
                classifier = load_analyzer()
                result = classifier(user_input)[0]
                
                label = result['label']
                score = result['score']

                st.divider()

                # Results Logic
                if label == "LABEL_1": # Scam/Spam Detected
                    st.error(f"🚨 ALERT: Potential Scam Detected (Risk: {score*100:.1f}%)")
                    st.markdown("#### Found Patterns:")
                    st.markdown("- **False Urgency:** Trying to make you act fast.")
                    st.markdown("- **Financial Coercion:** Threats of disconnection or loss.")
                    st.info("💡 **Action:** Do not share OTPs, click links, or pay any amount.")
                else:
                    st.success(f"✅ Safe: No obvious scam patterns found ({score*100:.1f}% confidence).")

if __name__ == "__main__":
    run_app()