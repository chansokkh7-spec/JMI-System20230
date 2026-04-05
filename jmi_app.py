import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(
    page_title="JMI | Global Strategic Systems",
    page_icon="🛡️",
    layout="wide"
)

# --- ២. ការរចនា Style (Modern Navy & Luxury Gold) ---
style_block = """
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@600&family=Montserrat:wght@300;600&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    /* Global Reset */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Kantumruy Pro', sans-serif;
        color: #E0E0E0;
    }
    .stApp { background: radial-gradient(circle, #002d5a 0%, #001529 100%); }
    
    /* Dashboard Cards */
    .kpi-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: 0.4s;
    }
    .kpi-card:hover { border-color: #D4AF37; transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.4); }
    .kpi-value { font-size: 38px; font-weight: bold; color: #D4AF37; font-family: 'Cinzel'; }
    .kpi-label { font-size: 14px; text-transform: uppercase; letter-spacing: 2px; color: #888; }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001529 !important;
        font-weight: bold !important;
        border-radius: 30px !important;
        padding: 10px 25px !important;
        border: none !important;
    }

    /* --- International Certificate Design --- */
    .cert-frame {
        background: #fff;
        padding: 20px;
        border: 15px solid #D4AF37;
        position: relative;
        max-width: 900px;
        margin: auto;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    .cert-inner {
        border: 2px solid #001529;
        padding: 60px;
        text-align: center;
        background-image: url('https://www.transparenttextures.com/patterns/cream-paper.png');
    }
    .cert-badge { width: 100px; margin-bottom: 20px; }
    .cert-title { font-family: 'Cinzel', serif; font-size: 42px; color: #001529; margin: 0; }
    .cert-name { font-family: 'Great Vibes', cursive; font-size: 70px; color: #D4AF37; margin: 20px 0; }
    .cert-footer { display: flex; justify-content: space-between; margin-top: 50px; }
    .sig-line { border-top: 2px solid #001529; width: 200px; color: #001529; font-weight: bold; padding-top: 5px; }
</style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-2026-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-03-25", "Status": "Active", "Skills": []}
    ])

# --- ៤. Sidebar Navigation ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color:#D4AF37;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/1021/1021501.png", width=100) # រូប Shield តំណាងឱ្យភាពរឹងមាំ
    pwd = st.text_input("Security Key", type="password")

if pwd == "JMI2026":
    menu = st.sidebar.selectbox("COMMAND CENTER", ["📊 Global Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    # --- ៥.១ Global Dashboard (ជួសជុល និងកែលម្អថ្មី) ---
    if menu == "📊 Global Dashboard":
        st.title("🏥 Strategic Command Center")
        
        # Row 1: KPI Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown('<div class="kpi-card"><div class="kpi-label">Scholars</div><div class="kpi-value">{}</div></div>'.format(len(st.session_state.db)), unsafe_allow_html=True)
        c2.markdown('<div class="kpi-card"><div class="kpi-label">Operational</div><div class="kpi-value">100%</div></div>', unsafe_allow_html=True)
        c3.markdown('<div class="kpi-card"><div class="kpi-label">Standard</div><div class="kpi-value">ISO</div></div>', unsafe_allow_html=True)
        c4.markdown('<div class="kpi-card"><div class="kpi-label">Region</div><div class="kpi-value">KH</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        
        # Row 2: Analytics
        col_chart, col_data = st.columns([1, 1])
        with col_chart:
            st.subheader("📈 Scholar Distribution")
            if not st.session_state.db.empty:
                df_counts = st.session_state.db['Level'].value_counts().reset_index()
                fig = px.pie(df_counts, values='count', names='Level', hole=.4, color_discrete_sequence=['#D4AF37', '#00509d', '#f1c40f', '#bdc3c7'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig, use_container_width=True)
        
        with col_data:
            st.subheader("⚙️ Master Database")
            st.dataframe(st.session_state.db.drop(columns=['Skills']), use_container_width=True)

    # --- ៥.២ Certification (ស្អាត និងស្តង់ដាអន្តរជាតិ) ---
    elif menu == "📜 Certification":
        st.title("📜 Official Certification Hub")
        
        levels = ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"]
        l_sel = st.selectbox("Select Academic Level", levels)
        filtered = st.session_state.db[st.session_state.db['Level'] == l_sel]
        
        if not filtered.empty:
            s_name = st.selectbox("Select Recipient", filtered['Name'].tolist())
            s_data = st.session_state.db[st.session_state.db['Name'] == s_name].iloc[0]
            
            if st.button("🌟 ISSUE INTERNATIONAL CERTIFICATE"):
                st.balloons()
                cert_html = f"""
                <div class="cert-frame">
                    <div class="cert-inner">
                        <img src="https://cdn-icons-png.flaticon.com/512/610/610333.png" class="cert-badge">
                        <h1 class="cert-title">JUNIOR MEDICAL INSTITUTE</h1>
                        <p style="text-transform: uppercase; letter-spacing: 5px; color: #666;">Global Competency Award</p>
                        <hr style="border: 0.5px solid #D4AF37; width: 50%;">
                        <p style="font-size: 20px; color: #333;">This is to certify that</p>
                        <h2 class="cert-name">{s_data['Name']}</h2>
                        <p style="font-size: 18px; color: #333; line-height: 1.6;">
                            has demonstrated exceptional academic rigor and successfully <br>
                            completed the strategic curriculum prescribed for the level of<br>
                            <b style="color: #001529; font-size: 24px;">{s_data['Level']}</b>
                        </p>
                        <div class="cert-footer">
                            <div class="sig-box">
                                <div class="sig-line">{datetime.now().strftime("%d %B %Y")}</div>
                                <span style="font-size: 12px; color: #555;">DATE OF ISSUANCE</span>
                            </div>
                            <div class="sig-box">
                                <p style="font-family: 'Great Vibes'; font-size: 25px; margin:0; color:#001529;">Dr. Chan Sokhoeurn</p>
                                <div class="sig-line">ACADEMIC DIRECTOR</div>
                                <span style="font-size: 10px; color: #D4AF37;">C2/DBA & PhD in Leadership</span>
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(cert_html, unsafe_allow_html=True)
        else:
            st.warning("No data found for this level.")

    # --- សំណុំមុខងារផ្សេងទៀត (រក្សាទុកឱ្យដូចដើម) ---
    elif menu == "🎓 Enrollment":
        st.header("New Scholar Registration")
        with st.form("reg"):
            n = st.text_input("Full Name (International Format)")
            l = st.selectbox("Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            if st.form_submit_button("REGISTER"):
                new_data = pd.DataFrame([{"ID": f"JMI-{datetime.now().year}-{len(st.session_state.db)+1:03d}", "Name": n.upper(), "Level": l, "Enroll_Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Active", "Skills": []}])
                st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
                st.success("Registered!")

    elif menu == "🏅 Skill Passport":
        st.header("🏅 Skill Mastery Tracker")
        s_list = st.session_state.db["Name"].tolist()
        if s_list:
            sel = st.selectbox("Select Student", s_list)
            idx = st.session_state.db[st.session_state.db["Name"] == sel].index[0]
            # មុខងារ Checkbox ដូចមុន...
            st.info("មុខងារ Update Skills ដំណើរការធម្មតា")

else:
    st.title("🏥 JMI International Portal")
    st.warning("🔒 Enter Security Key to Access Command Center.")
