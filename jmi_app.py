import streamlit as st
import pandas as pd
try:
    import plotly.express as px
except ImportError:
    st.error("សូមបង្កើត file ឈ្មោះ requirements.txt ក្នុង GitHub រួចដាក់ពាក្យ plotly ចូល។")

from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- ២. ការរចនា Style បែប Luxury Midnight & Multi-Color Highlights ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@600&family=Montserrat:wght@300;400;600&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    .stApp { 
        background: radial-gradient(circle, #002d5a 0%, #001529 100%);
        color: #E6E9ED !important; 
        font-family: 'Montserrat', 'Kantumruy Pro', sans-serif;
    }
    .stMarkdown, p, span, label, li, div { color: #E6E9ED !important; }
    h1, h2, h3 { font-family: 'Cinzel', serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }

    /* ប៊ូតុងទូទៅ */
    .stButton>button {
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 24px !important;
        width: 100%;
        transition: 0.3s;
        font-weight: 600 !important;
    }

    /* --- ពណ៌តាម Module នីមួយៗ --- */
    /* 1. Dashboard Style (Gold) */
    .header-dashboard { color: #D4AF37 !important; border-left: 5px solid #D4AF37; padding-left: 15px; }
    .card-dashboard { background: rgba(212, 175, 55, 0.1); border: 1px solid #D4AF37; border-radius: 15px; padding: 20px; text-align: center; }

    /* 2. Enrollment Style (Emerald Green) */
    .header-enroll { color: #2ECC71 !important; border-left: 5px solid #2ECC71; padding-left: 15px; }
    .form-enroll { background: rgba(46, 204, 113, 0.05); border: 1px solid #2ECC71; border-radius: 15px; padding: 30px; }
    .btn-enroll button { background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%) !important; color: white !important; }

    /* 3. Certification Style (Royal Blue) */
    .header-cert { color: #3498DB !important; border-left: 5px solid #3498DB; padding-left: 15px; }
    .btn-cert button { background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%) !important; color: white !important; }

    /* Certificate View (White/Gold) */
    .cert-container {
        background: #fff; padding: 35px; border: 18px solid #D4AF37; max-width: 850px; margin: auto;
        color: #001529 !important; box-shadow: 0 0 60px rgba(0,0,0,0.7);
    }
    .cert-inner { border: 2px solid #001529; padding: 40px; text-align: center; }
    .cert-inner h1, .cert-inner p, .cert-inner b, .cert-inner td { color: #001529 !important; }
    .cert-name { font-family: 'Great Vibes', cursive; font-size: 75px; color: #B8860B !important; margin: 15px 0; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #001529 !important; border-right: 1px solid rgba(212, 175, 55, 0.2); }
</style>
""", unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-2026-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-03-25", "Status": "Active"}
    ])

# --- ៤. Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color:#D4AF37;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Security Access Key", type="password")

if pwd == "JMI2026":
    menu = st.sidebar.radio("CHOOSE MODULE", ["📊 Dashboard", "🎓 Enrollment", "📜 Certification"])

    # --- ៥.១ Dashboard (Gold Theme) ---
    if menu == "📊 Dashboard":
        st.markdown("<h1 class='header-dashboard'>JMI Command Center</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="card-dashboard"><h3>Total Scholars</h3><h1 style="color:#D4AF37">{len(st.session_state.db)}</h1></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="card-dashboard"><h3>System Integrity</h3><h1 style="color:#2ECC71">Secure</h1></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="card-dashboard"><h3>Academic Year</h3><h1 style="color:#D4AF37">2026</h1></div>', unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        col_chart, col_table = st.columns([1.2, 1])
        with col_chart:
            df_counts = st.session_state.db['Level'].value_counts().reset_index()
            fig = px.pie(df_counts, values='count', names='Level', hole=.4, color_discrete_sequence=['#D4AF37', '#3498DB', '#2ECC71'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", title="Scholarship Breakdown")
            st.plotly_chart(fig, use_container_width=True)
        with col_table:
            st.subheader("Registry List")
            st.dataframe(st.session_state.db[["ID", "Name", "Level"]], use_container_width=True)

    # --- ៥.២ Enrollment (Green Theme) ---
    elif menu == "🎓 Enrollment":
        st.markdown("<h1 class='header-enroll'>New Scholar Registration</h1>", unsafe_allow_html=True)
        st.markdown("<div class='form-enroll'>", unsafe_allow_html=True)
        with st.form("enroll", clear_on_submit=True):
            name = st.text_input("Full Name (Uppercase)")
            level = st.selectbox("Academic Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            st.markdown("<div class='btn-enroll'>", unsafe_allow_html=True)
            submit = st.form_submit_button("COMPLETE REGISTRATION")
            st.markdown("</div>", unsafe_allow_html=True)
            if submit and name:
                new_id = f"JMI-2026-{len(st.session_state.db)+1:03d}"
                new_data = pd.DataFrame([{"ID": new_id, "Name": name.upper(), "Level": level, "Enroll_Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Active"}])
                st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
                st.success(f"System: {name.upper()} successfully enrolled!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ៥.៣ Certification (Blue Theme) ---
    elif menu == "📜 Certification":
        st.markdown("<h1 class='header-cert'>Certification Hub</h1>", unsafe_allow_html=True)
        selected_name = st.selectbox("Search Scholar Name:", st.session_state.db['Name'].tolist())
        s_info = st.session_state.db[st.session_state.db['Name'] == selected_name].iloc[0]
        
        st.markdown("<div class='btn-cert'>", unsafe_allow_html=True)
        if st.button("ISSUE OFFICIAL CERTIFICATE"):
            st.balloons()
            cert_html = f"""
            <div class="cert-container">
                <div class="cert-inner">
                    <h1 style="font-size: 35px;">JUNIOR MEDICAL INSTITUTE</h1>
                    <p style="letter-spacing: 3px; font-weight: bold; font-size: 12px;">PRE-MEDICAL EXCELLENCE PROGRAM</p>
                    <hr style="border: 1px solid #D4AF37; width: 40%;">
                    <p style="font-size: 18px; font-style: italic;">This honors the achievement of</p>
                    <h2 class="cert-name">{s_info['Name']}</h2>
                    <p style="font-size: 18px;">Upon successful completion of the academic requirements for</p>
                    <h3 style="color: #001529 !important; font-size: 25px;">{s_info['Level']}</h3>
                    <br><br>
                    <table style="width: 100%;">
                        <tr>
                            <td><b>{datetime.now().strftime("%B %d, %Y")}</b><br><small>DATE</small></td>
                            <td><b>Dr. Chan Sokhoeurn</b><br><small>ACADEMIC DIRECTOR</small></td>
                        </tr>
                    </table>
                </div>
            </div>
            """
            st.markdown(cert_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("🔒 JMI Executive Key Required.")
