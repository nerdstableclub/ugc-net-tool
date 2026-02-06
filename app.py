import streamlit as st
import pandas as pd

# --- 1. PASSWORD PROTECTION SYSTEM ---
# This ensures that unless the repo is public, anyone can access it via your site without a Google Login
def check_password():
    def password_entered():
        if st.session_state["password"] == "NET2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔐 NerdsTable Premium Access")
        st.text_input("Enter the Access Code (NET2026):", type="password", on_change=password_entered, key="password")
        st.info("This predictor is exclusive to NerdSchool students.")
        return False
    elif not st.session_state["password_correct"]:
        st.title("🔐 NerdsTable Premium Access")
        st.text_input("Enter the Access Code (NET2026):", type="password", on_change=password_entered, key="password")
        st.error("😕 Incorrect Code. Please check your course dashboard.")
        return False
    else:
        return True

# --- 2. THE MAIN APP (Only runs if password is correct) ---
if check_password():
    # --- PAGE CONFIGURATION ---
    st.set_page_config(page_title="UGC NET High-Yield Predictor", page_icon="📚")

    # --- LOAD DATA FUNCTION (Your Original Logic) ---
    @st.cache_data
    def load_data():
        try:
            df = pd.read_csv("FINAL_DATABASE.csv")
            if 'Key Fact' in df.columns:
                df = df.rename(columns={'Key Fact': 'Key Exam Fact'})
            if 'Found in Years' in df.columns:
                df = df.rename(columns={'Found in Years': 'Years Found'})
            
            df['Topic'] = df['Topic'].astype(str)
            df['Key Exam Fact'] = df.get('Key Exam Fact', pd.Series(["No data available"] * len(df))).astype(str)
            df['Years Found'] = df.get('Years Found', pd.Series([""] * len(df))).astype(str)
            return df
        except FileNotFoundError:
            return None

    df = load_data()

    # --- HEADER ---
    st.title("📚 UGC NET English: High-Yield Predictor")
    st.write("Type a topic (Author, Work, or Theory) to see its exam probability.")

    # --- SEARCH BAR ---
    query = st.text_input("🔍 Search Topic", placeholder="e.g., Chaucer, T.S. Eliot, Post-colonialism")

    # --- SEARCH LOGIC (Your Original Logic) ---
    if query:
        if df is not None:
            results = df[df['Topic'].str.contains(query, case=False, na=False)]

            if not results.empty:
                st.success(f"Found {len(results)} matches for '{query}'")
                
                for index, row in results.iterrows():
                    with st.container():
                        st.markdown("---")
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.subheader(row['Topic'])
                            st.write(f"**💡 Key Exam Fact:** {row['Key Exam Fact']}")
                            st.caption(f"📅 Found in: {row['Years Found']}")
                        
                        with col2:
                            score = row['Yield Score']
                            if score >= 20:
                                st.error(f"🔥 CRITICAL\n(Score: {score})")
                            elif score >= 10:
                                st.warning(f"✅ HIGH YIELD\n(Score: {score})")
                            else:
                                st.info(f"⚠️ REVIEW\n(Score: {score})")
            else:
                st.warning("No specific data found for this topic. It might be low yield or spelled differently.")
        else:
            st.error("⚠️ Database file 'FINAL_DATABASE.csv' not found. Please run the analysis script first.")

    # --- FOOTER ---
    st.markdown("---")
    st.markdown("*Tool developed by NerdsTable*")
    if st.sidebar.button("Log Out"):
        st.session_state["password_correct"] = False
        st.rerun()
