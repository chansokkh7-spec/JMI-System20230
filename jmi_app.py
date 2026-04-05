import streamlit as st
import pandas as pd

# រៀបចំទំព័រ
st.set_page_config(page_title="JMI Portal", page_icon="🏥")

st.title("🏥 ប្រព័ន្ធគ្រប់គ្រង Junior Medical Institute (JMI)")
st.subheader("បណ្តុះបណ្តាលគ្រូពេទ្យជំនាន់ក្រោយ")

# បង្កើតតារាងទិន្នន័យបណ្តោះអាសន្ន
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["អត្តសញ្ញាណ", "ឈ្មោះសិស្ស", "កម្រិតសិក្សា", "ជំនាញ"])

# ផ្នែកបញ្ចូលទិន្នន័យ
with st.expander("➕ ចុះឈ្មោះសិស្ស JMI ថ្មី"):
    id_s = st.text_input("លេខសម្គាល់ (ID)")
    name_s = st.text_input("ឈ្មោះពេញ")
    level_s = st.selectbox("ថ្នាក់សិក្សា", ["Preschool", "Primary", "Secondary", "High School"])
    skill_s = st.text_input("ជំនាញ (ឧ. First Aid)")
    
    if st.button("រក្សាទុកទិន្នន័យ"):
        new_data = pd.DataFrame([[id_s, name_s, level_s, skill_s]], columns=st.session_state.df.columns)
        st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
        st.success("បានបញ្ចូលទិន្នន័យសិស្សជោគជ័យ!")

# បង្ហាញបញ្ជីឈ្មោះ
st.write("### 📋 បញ្ជីឈ្មោះសិស្សក្នុងប្រព័ន្ធ")
st.table(st.session_state.df)
