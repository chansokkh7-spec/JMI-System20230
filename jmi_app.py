import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(
    page_title="JMI | International Strategic Portal",
    page_icon="🏥",
    layout="wide"
)

# --- ២. ការរចនា Style (Navy Blue & Gold International Standard) ---
style_block = """
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    /* Global Styles */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Kantumruy Pro', sans-serif;
        color: #ffffff;
    }
    .stApp { background-color: #001f3f; }
    
    /* Checkbox Visibility */
    .stCheckbox label p {
        color: #D4AF37 !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Cinzel', serif; }
    
    /* Metrics Card Style */
    .metric-card {
        background: linear-gradient(135deg, #002d5a 0%, #001f3f 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #D4AF37;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .metric-title { font-size: 14px; color: #D4AF37; text-transform: uppercase; letter-spacing: 1px;}
    .metric-value { font-size: 35px; font-weight: bold; color: #ffffff; margin: 5px 0; }

    /* Button Style */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001f3f !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #D4AF37; }

    /* --- International Certificate Style --- */
    .cert-outer {
        background: #fdfdfd;
        padding: 15px;
        border: 12px solid #D4AF37;
        max-width: 950px;
        margin: auto;
        box-shadow: 0 0 50px rgba(0,0,0,0.5);
    }
    .cert-inner {
        border: 4px double #001f3f;
        padding: 50px;
        text-align: center;
        background-image: url('https://www.transparenttextures.com/patterns/handmade-paper.png');
    }
    .cert-header { font-family: 'Cinzel', serif; font-size: 45px; color: #001f3f; margin-bottom: 0; }
    .cert-sub-header { font-size: 18px; letter-spacing: 4px; color: #666; margin-top: 5px; text-transform: uppercase; }
    .cert-name { font-family: 'Great Vibes', cursive; font-size: 75px; color: #D4AF37; margin: 25px 0; }
    .cert-body { font-family: 'DM Serif Display', serif; font-size: 22px; color: #333; line-height: 1.5; }
    .cert-footer { margin-top: 60px; display: flex; justify-content: space-between; align-items: flex-end; padding: 0 40px; }
    .sig-box { width: 250px; text-align: center; color: #001f3f; }
    .sig-line { border-top: 2px solid #001f3f; margin-bottom: 5px; }
</style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ (Session State) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-03-25", "Status": "Active", "Skills": []},
        {"ID": "JMI-002", "Name": "DARA VICHET", "Level": "អនុវិទ្យាល័យ", "Enroll_Date": "2026-03-26", "Status": "Active", "Skills": []}
    ])

# --- ៤. Sidebar ---
st.sidebar.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<center><h1 style='font-size:60px; color: #D4AF37;'>🛡️</h1></center>", unsafe_allow_html=True)
pwd = st.sidebar.text_input("Director's Key", type="password")

if pwd == "JMI2026":
    menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    def get_lessons(level):
        return [f"មេរៀនទី {i}" for i in range(1, 10)] if level in ["មត្តេយ្យ", "បឋម"] else [f"មេរៀនទី {i}" for i in range(1, 13)]

    # --- ៥.១ Dashboard (International Standard) ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Command Center")
        
        # Top Metrics
        m1, m2, m3 = st.columns(3)
        with m1: st.markdown(f'<div class="metric-card"><div class="metric-title">Total Scholars</div><div class="metric-value">{len(st.session_state.db)}</div></div>', unsafe_allow_html=True)
        with m2: st.markdown(f'<div class="metric-card"><div class="metric-title">Status</div><div class="metric-value">Operational</div></div>', unsafe_allow_html=True)
        with m3: st.markdown(f'<div class="metric-card"><div class="metric-title">Year</div><div class="metric-value">2026</div></div>', unsafe_allow_html=True)
        
        # Charts Area
        st.markdown("### 📈 បូកសរុបទិន្នន័យតាមក
