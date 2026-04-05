import streamlit as st
import pandas as pd
try:
    import plotly.express as px
except ImportError:
    st.error("សូមបង្កើត file ឈ្មោះ requirements.txt ក្នុង GitHub រួចដាក់ពាក្យ plotly ចូល។")

from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី (Standard Config) ---
st.set_page_config(
    page_title="JMI | Strategic Management Portal",
    page_icon="🛡️",
    layout="wide"
)

# --- ២. ការរចនា Style បែប Luxury Midnight & Gold ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@600&family=Montserrat:wght@300;400;600&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
<style>
    /* កំណត់ផ្ទៃខាងក្រោយ និងពុម្ពអក្សរទូទៅ */
    .stApp { 
        background: radial-gradient(circle, #002d5a 0%, #001529 100%);
        color: #E6E9ED !important; 
        font-family: 'Montserrat', 'Kantumruy Pro', sans-serif;
    }
    
    /* កែពណ៌អក្សរទូទៅឱ្យទៅជា Off-White ដើម្បីឱ្យច្បាស់ត្រជាក់ភ្នែក */
    .stMarkdown, p, span, label, li, div {
        color: #E6E9ED !important;
    }

    /* ពណ៌ចំណងជើង (Royal Gold) */
    h1, h2, h3 { 
        color: #D4AF37 !important; 
        font-family: 'Cinzel', serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* រចនា Dashboard Card ឱ្យមានភាពថ្លាៗ (Glassmorphism) */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: 0.3s ease;
    }
    .metric-card:hover {
        border: 1px solid #D4AF37;
        transform: translateY(-5px);
    }
    .metric-card h3 { font-size: 14px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; }
    .metric-value { font-size: 40px; font-weight: bold; color: #D4AF37 !important; font-family: 'Cinzel'; }

    /* ប៊ូតុង Premium Gold */
    .stButton>button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001529 !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 24px !important;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.5);
        transform: scale(1.02);
    }

    /* --- Luxury International Certificate --- */
    .cert-container {
        background: #fff;
        padding: 35px;
        border: 18px solid #D4AF37;
        max-width: 900px;
        margin: auto;
        color: #001529 !important;
        box-shadow: 0 0 60px rgba(0,0,0,0.7);
        position: relative;
    }
    .cert-inner {
        border: 2px solid #001529;
        padding: 45px;
        text-align: center;
        background-image: url('https://www.transparenttextures.com/patterns/cream-paper.png');
    }
    /* បង្ខំឱ្យអក្សរក្នុង Certificate ទៅជាពណ៌ខ្មៅ ឬមាស ដើម្បីមើលឃើញលើផ្ទៃស */
    .cert-inner h1, .cert-inner p, .cert-inner b, .cert-inner small, .cert-inner td {
        color: #001529 !important;
    }
    .cert-name { 
        font-family: 'Great Vibes', cursive; 
        font-size: 80px; 
        color: #B8860B !important; 
        margin: 15px 0;
        text-shadow: none;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #001529 !important;
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ (Database) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-2026-001", "Name": "CHAN SOKHOEURN", "Level": "វិទ្យាល័យ", "Enroll_Date": "2026-03-25", "Status": "Active"}
    ])

# --- ៤. Sidebar Navigation ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color:#D4AF37;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("<center><h1 style='font-size:60px; margin:0;'>🛡️</h1></center>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Security Access Key", type="password")

if pwd == "JMI2026":
    menu = st.sidebar.radio("COMMAND CENTER", ["📊 Dashboard", "🎓 Enrollment", "📜 Certification"])

    # --- ៥.១ Dashboard (Premium Analytics) ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Command Center")
        
        # Top KPI Metrics
        c1, c2, c3 = st.columns(3)
        with c1: 
            st.markdown(f'<div class="metric-card"><h3>Total Scholars</h3><div class="metric-value">{len(st.session_state.db)}</div></div>', unsafe_allow_html=True)
        with c2: 
            st.markdown('<div class="metric-card"><h3>System Integrity</h3><div class="metric-value">100%</div></div>', unsafe_allow_html=True)
        with c3: 
            st.markdown('<div class="metric-card"><h3>Academic Year</h3><div class="metric-value">2026</div></div>', unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        
        # Analytical Charts
        col_chart, col_table = st.columns([1.2, 1])
        
        with col_chart:
            st.subheader("📈 Scholar Enrollment Distribution")
            if not st.session_state.db.empty:
                df_counts = st.session_state.db['Level'].value_counts().reset_index()
                fig = px.pie(df_counts, values='count', names='Level', hole=.4,
                             color_discrete_sequence=['#D4AF37', '#00509d', '#f1c40f', '#bdc3c7'])
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)', 
                    font_color="#E6E9ED",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col_table:
            st.subheader("📂 Master Registry")
            st.dataframe(st.session_state.db[["ID", "Name", "Level"]], use_container_width=True)

    # --- ៥.២ Enrollment ---
    elif menu == "🎓 Enrollment":
        st.header("Scholastic Enrollment Form")
        with st.form("enroll", clear_on_submit=True):
            name = st.text_input("Scholar Full Name (International Format)")
            level = st.selectbox("Academic Level", ["មត្តេយ្យ", "បឋម", "អនុវិទ្យាល័យ", "វិទ្យាល័យ"])
            if st.form_submit_button("REGISTER TO SYSTEM"):
                new_id = f"JMI-{datetime.now().year}-{len(st.session_state.db)+1:03d}"
                new_data = pd.DataFrame([{"ID": new_id, "Name": name.upper(), "Level": level, "Enroll_Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Active"}])
                st.session_state.db = pd.concat([st.session_state.db, new_data], ignore_index=True)
                st.success(f"Confirmed: {name} has been securely enrolled.")

    # --- ៥.៣ Certification (Luxury Standard) ---
    elif menu == "📜 Certification":
        st.title("📜 Official Certification Hub")
        if not st.session_state.db.empty:
            selected_name = st.selectbox("Select Scholar for Issuance:", st.session_state.db['Name'].tolist())
            s_info = st.session_state.db[st.session_state.db['Name'] == selected_name].iloc[0]
            
            if st.button("🌟 GENERATE OFFICIAL CERTIFICATE"):
                st.balloons()
                cert_html = f"""
                <div class="cert-container">
                    <div class="cert-inner">
                        <h1 style="font-size: 40px; margin-bottom: 5px;">JUNIOR MEDICAL INSTITUTE</h1>
                        <p style="letter-spacing: 5px; font-weight: 600; font-size: 14px; color: #666 !important;">INTERNATIONAL ACADEMIC EXCELLENCE</p>
                        <div style="margin: 25px auto; width: 50%; border-bottom: 2px solid #D4AF37;"></div>
                        <p style="font-size: 20px; font-style: italic;">This prestigious award is presented to</p>
                        <h2 class="cert-name">{s_info['Name']}</h2>
                        <p style="font-size: 19px;">For demonstrating exceptional academic rigor and <br>mastering the medical curriculum for the level of</p>
                        <p style="font-size: 28px; font-weight: bold; text-decoration: underline; color: #001529 !important;">{s_info['Level']}</p>
                        <br><br>
                        <table style="width: 100%; border: none;">
                            <tr>
                                <td style="text-align: center; width: 50%;">
                                    <div style="border-top: 1.5px solid #001529; width: 200px; margin: auto; padding-top: 10px;">
                                        <b style="font-size: 16px;">{datetime.now().strftime("%B %d, %Y")}</b><br>
                                        <small style="text-transform: uppercase; letter-spacing: 1px;">Date of Issuance</small>
                                    </div>
                                </td>
                                <td style="text-align: center; width: 50%;">
                                    <div style="border-top: 1.5px solid #001529; width: 200px; margin: auto; padding-top: 10px;">
                                        <b style="font-size: 18px; font-family: 'Cinzel';">Dr. Chan Sokhoeurn</b><br>
                                        <small style="text-transform: uppercase; letter-spacing: 1px;">Academic Director</small>
                                    </div>
                                </td>
                            </tr>
                        </table>
                        <div style="margin-top: 30px;">
                             <small style="color: #D4AF37 !important;">C2/DBA & PhD in Leadership</small>
                        </div>
                    </div>
                </div>
                """
                st.markdown(cert_html, unsafe_allow_html=True)
        else:
            st.warning("No scholars found in registry.")

else:
    st.title("🏥 JMI Strategic Management Portal")
    st.info("🔒 Restricted Access: Please enter Executive Key to synchronize with the command center.")
