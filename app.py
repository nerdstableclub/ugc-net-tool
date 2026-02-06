import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="UGC NET High-Yield Predictor", page_icon="📚")

# --- LOAD DATA FUNCTION ---
@st.cache_data
def load_data():
    try:
        # Load the CSV
        df = pd.read_csv("FINAL_DATABASE.csv")
        
        # --- FIX COLUMN NAMES (Standardize them) ---
        # This fixes the "KeyError" by renaming whatever column exists to the standard one
        if 'Key Fact' in df.columns:
            df = df.rename(columns={'Key Fact': 'Key Exam Fact'})
        if 'Found in Years' in df.columns:
            df = df.rename(columns={'Found in Years': 'Years Found'})
            
        # Ensure text columns are strings
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

# --- LOGIC ---
if query:
    if df is not None:
        # Filter: Search inside the 'Topic' column (case insensitive)
        results = df[df['Topic'].str.contains(query, case=False, na=False)]

        if not results.empty:
            st.success(f"Found {len(results)} matches for '{query}'")
            
            for index, row in results.iterrows():
                # CREATE THE CARD
                with st.container():
                    st.markdown("---")
                    
                    # COLUMNS FOR LAYOUT
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.subheader(row['Topic'])
                        st.write(f"**💡 Key Exam Fact:** {row['Key Exam Fact']}")
                        st.caption(f"📅 Found in: {row['Years Found']}")
                    
                    with col2:
                        # DYNAMIC COLOR BADGES
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