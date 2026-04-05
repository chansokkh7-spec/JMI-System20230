# --- MODULE 3: SKILL PASSPORT ---
elif menu == "📔 Skill Passport":
    st.markdown("<h1 class='header-style'>📔 Skill Mastery Passport</h1>", unsafe_allow_html=True)
    if not st.session_state.db.empty:
        sel_student = st.selectbox("Select Student:", st.session_state.db['Name'].tolist())
        st.info(f"Scholar: {sel_student} | Level: {st.session_state.db[st.session_state.db['Name']==sel_student]['Level'].values[0]}")
        
        # បង្កើតប៊ូតុង Check all Lesson
        # នៅពេលចុចលើវា វានឹងទៅ Update តម្លៃក្នុង session_state នៃមេរៀននីមួយៗ
        master_check = st.checkbox("✅ Check all Lesson", key=f"master_{sel_student}")
        
        st.markdown("---")
        cols = st.columns(2)
        
        for i in range(1, 13):
            # បង្កើត key សម្រាប់មេរៀននីមួយៗ
            check_key = f"L{i}_{sel_student}"
            
            # បើ master_check ត្រូវបានគ្រីស នោះមេរៀនទាំងអស់នឹងត្រូវបានគ្រីសដោយស្វ័យប្រវត្តិ
            if master_check:
                st.session_state[check_key] = True
            
            with cols[0 if i <= 6 else 1]:
                st.checkbox(f"Medical Competency Module {i}", key=check_key)
    else:
        st.warning("NO DATA FOUND: ENROLL STUDENTS FIRST")
