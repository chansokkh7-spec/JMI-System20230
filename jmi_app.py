import streamlit as st
import pandas as pd
try:
    import plotly.express as px
except ImportError:
    st.error("សូមបង្កើត file ឈ្មោះ requirements.txt ក្នុង GitHub រួចដាក់ពាក្យ plotly ចូល។")

from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(page_title="JMI | Strategic Portal", page_icon="🏥", layout="wide")

# --- ២. ការរចនា Style (កែពណ៌អក្សរឱ្យទៅជាពណ៌ស) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    /* កំណត់ពណ៌ផ្ទៃខាងក្រោយ និងពណ៌អក្សរទូទៅជាពណ៌ស */
    .stApp { 
        background-color: #001f3f; 
        color: #ffffff !important; 
    }
    
    /* កំណត់ពណ៌អក្សរសម្រាប់ Markdown, Label និងអក្សរធម្មតា */
    .stMarkdown, p, span, label {
        color: #ffffff !important;
    }

    /* ពណ៌ចំណងជើងរក្សាទុកពណ៌មាសដដែលដើម្បីឱ្យស្អាត */
    h1, h2, h3 { 
        color: #D4AF37 !important; 
        font-family: 'Cinzel', serif; 
    }
    
    /* Dashboard Card */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid #D4AF37;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    .metric-card h3 { margin: 0; color: #D4AF37 !important; }

    /* Certificate Standard (រក្សាផ្ទៃស អក្សរខ្មៅ/មាស តាមស្តង់ដារសញ្ញាបត្រ) */
    .cert-container {
        background: white;
        padding: 30px;
        border: 15px solid #D4AF37;
        max-width: 900px;
        margin: auto;
        color: #001f3f !important;
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
    }
    .cert-container p, .cert-container h1, .cert-container h2, .cert-container b, .cert-container small {
        color: #001f3f !important;
    }
    .cert-inner {
        border: 2px solid #001f3f;
        padding: 50px;
        text-align: center;
    }
    .cert-title { font-size: 45px; margin-bottom: 10px; }
    .cert-name { 
        font-family: 'Great Vibes', cursive; 
        font-size: 70px; 
        color: #D4AF37 !important; 
        margin: 20px 0; 
    }
    .cert-text { font-size: 22px; margin: 20px 0; }

    /* កែពណ៌អក្សរក្នុង Sidebar */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-03-25", "Status": "Active"}
    ])

# --- ៤. Sidebar Navigation ---
st.sidebar.markdown("## JMI EXECUTIVE")
pwd = st.sidebar.text_input("Security Key", type="password")

if pwd == "JMI2026":
    menu = st.sidebar.radio("MODULES", ["📊 Dashboard", "🎓 Enrollment", "📜 Certification"])

    # --- ៥.១ Dashboard ថ្មី ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Command Center")
        
        # Metrics
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card"><h3>TOTAL SCHOLARS</h3><h1 style="color:#D4AF37">{len(st.session_state.db)}</h1></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="metric-card"><h3>SYSTEM STATUS</h3><h1 style="color:#00ff00">ONLINE</h1></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="metric-card"><h3>YEAR</h3><h1 style="color:#D4AF37">2026</h1></div>', unsafe_allow_html=True)
        
        st.write("---")
        
        # Analytics Chart
        try:
            df_counts = st.session_state.db['Level'].value_counts().reset_index()
            fig = px.bar(df_counts, x='Level', y='count', title="Scholar Distribution by Level",
                         color_discrete_sequence=['#D4AF37'])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font_color="white",
                title_font_color="white"
            )
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.info("កំពុងរង់ចាំការដំឡើង Plotly...")

        st.subheader("📋 Master Records")
        st.dataframe(st.session_state.db, use_container_width=True)

    # --- ៥.២ Enrollment ---
    elif menu == "🎓 Enrollment":
        st.header("Enroll New Scholar")
        with st.form("enroll"):
            name = st.text_input("Student Name (Full Name)")
            level = st.selectbox("Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            if st.form_submit_button("REGISTER NOW"):
                new_data = pd.DataFrame([{"ID": f"JMI-{len(st.session_state.db)+1:03d}", "Name": name.upper(), "Level": level, "Enroll_Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Active"}])
                st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
                st.success("Successfully Registered!")

    # --- ៥.៣ Certification ---
    elif menu == "📜 Certification":
        st.title("📜 Certification Generator")
        selected_name = st.selectbox("Select Student Name:", st.session_state.db['Name'].tolist())
        student_info = st.session_state.db[st.session_state.db['Name'] == selected_name].iloc[0]
        
        if st.button("🌟 GENERATE CERTIFICATE"):
            st.balloons()
            cert_html = f"""
            <div class="cert-container">
                <div class="cert-inner">
                    <h1 class="cert-title">JUNIOR MEDICAL INSTITUTE</h1>
                    <p style="letter-spacing: 5px; font-weight: bold;">CERTIFICATE OF COMPLETION</p>
                    <hr style="border: 1px solid #D4AF37; width: 50%;">
                    <p class="cert-text">This award is proudly presented to</p>
                    <h2 class="cert-name">{student_info['Name']}</h2>
                    <p class="cert-text">For outstanding academic achievement in the level of<br>
                    <b style="font-size: 30px; border-bottom: 2px solid #D4AF37;">{student_info['Level']}</b></p>
                    <br><br>
                    <div style="border-top: 2px solid #333; width: 200px; margin: auto;">
                        <p style="margin: 0; font-weight: bold;">Dr. Chan Sokhoeurn</p>
                        <small>Director of JMI</small>
                    </div>
                </div>
            </div>
            """
            st.markdown(cert_html, unsafe_allow_html=True)

else:
    st.info("🔒 សូមបញ្ចូលកូដសម្ងាត់ដើម្បីចូលប្រើប្រាស់។")
