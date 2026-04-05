import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🛡️", layout="wide")

# --- 2. Luxury UI Styling ---
st.markdown("""
<style>
    .stApp { background: radial-gradient(circle, #002d5a 0%, #001529 100%); }
    [data-testid="stSidebar"] { background-color: #001529 !important; border-right: 2px solid #D4AF37; }
    html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span, label, h1, h2, h3, .stMetric {
        color: #D4AF37 !important; font-family: 'Inter', sans-serif;
    }
    .stButton>button { 
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%) !important;
        color: #001529 !important; border-radius: 8px !important; font-weight: bold !important; border: none !important;
    }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. Database Engine ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-001", "Name": "CHAN SOKHOEURN", "Level": "HIGH SCHOOL", "Fee": 500.0, "Paid": "PAID", "Date": "2026-03-25"},
        {"ID": "JMI-002", "Name": "SOK SAMBATH", "Level": "PRIMARY SCHOOL", "Fee": 250.0, "Paid": "PAID", "Date": "2026-03-26"},
        {"ID": "JMI-003", "Name": "MEA LINA", "Level": "KINDERGARTEN", "Fee": 200.0, "Paid": "UNPAID", "Date": "2026-03-27"}
    ])

# --- 4. Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>JMI EXECUTIVE</h2>", unsafe_allow_html=True)
    st.markdown("---")
    pwd = st.text_input("Director's Key", type="password")
    if pwd == "JMI2026":
        choice = st.radio("STRATEGIC MODULES", ["Dashboard", "Enrollment", "Skill Passport", "Certification", "Financial Hub"])
    else:
        st.stop()

# --- MODULE 1: DASHBOARD (FIXED CHARTS) ---
if choice == "Dashboard":
    st.markdown("<h1>📊 JMI Strategic Analytics</h1>", unsafe_allow_html=True)
    
    # Summary Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Scholars", len(st.session_state.db))
    m2.metric("Total Revenue", f"${st.session_state.db[st.session_state.db['Paid'] == 'PAID']['Fee'].sum():,.2f}")
    m3.metric("Pending Fees", f"${st.session_state.db[st.session_state.db['Paid'] == 'UNPAID']['Fee'].sum():,.2f}")
    
    st.markdown("---")
    
    # ក្រាហ្វិក (Charts)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎓 Enrollment by Level")
        # កែសម្រួលពណ៌ត្រង់នេះដើម្បីកុំឱ្យមាន Error
        jmi_colors = ['#D4AF37', '#B8860B', '#FFD700', '#DAA520'] 
        fig_pie = px.pie(
            st.session_state.db, 
            names='Level', 
            color_discrete_sequence=jmi_colors, 
            hole=0.4
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            font_color="#D4AF37", 
            legend_font_color="#D4AF37"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col2:
        st.subheader("💵 Payment Analysis")
        fig_bar = px.bar(
            st.session_state.db, 
            x='Paid', 
            y='Fee', 
            color='Paid', 
            color_discrete_map={'PAID': '#D4AF37', 'UNPAID': '#C62828'}
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color="#D4AF37",
            xaxis_title="Status",
            yaxis_title="Total Fee ($)"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Enrollment Database")
    st.dataframe(st.session_state.db, use_container_width=True)

# (ផ្នែកផ្សេងៗទៀត Enrollment, Skill Passport, ទុកនៅដដែល...)
