from pathlib import Path
import pandas as pd
import streamlit as st

# Configure the page layout to use wide mode for full width tables
st.set_page_config(
    page_title="Charleville LTC Ladies Box League",
    page_icon="🎾",
    layout="wide",
)

# --- CUSTOM CSS FOR POLISHED UI ---
st.markdown(
    """
    <style>
        html, body, #root, [data-testid="stAppViewContainer"] {
            touch-action: pan-x pan-y pinch-zoom;
        }

        /* Custom Header Banner with Court Background Image */
        .header-container {
            background: linear-gradient(135deg, rgba(58, 28, 93, 0.92), rgba(217, 72, 160, 0.88)); 
            padding: 2.5rem 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .header-container h1 {
            color: white !important;
            margin-bottom: 0.2rem;
        }
        .header-container p {
            color: #e8f5e9 !important;
            font-size: 1.1rem;
        }

        /* Card Styling for Results - Adapts to Light/Dark Mode */
        .result-card {
            background-color: var(--secondary-background-color);
            color: var(--text-color);
            padding: 1rem 1.2rem;
            border-radius: 8px;
            border-left: 5px solid #2ecc71;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 0.8rem;
            font-size: 1rem;
        }
        
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data(ttl=60)
def load_league_data(sheet_id, gid):
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    df = pd.read_csv(csv_url)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
    return df

@st.cache_data(ttl=60)
def load_results_data(sheet_id):
    try:
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Results"
        df = pd.read_csv(csv_url)
        return df
    except Exception:
        return pd.DataFrame()

# Styling function shade Total Points column safely for themes
def style_league_table(df):
        
    # Shade the 'Total Points' column using Streamlit conditional / neutral fallback colors
    
    if "Total Score" in df.columns:
        return df.style.set_properties(
            subset=["Total Score"],
            props="background-color: rgba(128, 128, 128, 0.2); font-weight: bold;",
        )
    return df.style

# Styled Header Banner
st.markdown(
    """
    <div class="header-container">
        <h1>Charleville LTC Ladies Box League</h1>
        <p>Live standings, results, and official league rules.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

try:
    sheet_config = st.secrets["sheets"]
    sheet_id = sheet_config["spreadsheet_id"]
    tolka_gid = sheet_config["tolka_gid"]
    liffey_gid = sheet_config["liffey_gid"]

    tolka_df = load_league_data(sheet_id, tolka_gid)
    liffey_df = load_league_data(sheet_id, liffey_gid)
    results_df = load_results_data(sheet_id)

    # Create 3 top-level tabs
    tab_tolka, tab_liffey, tab_rules = st.tabs([
        "Tolka Division", 
        "Liffey Division", 
        "League Rules"
    ])

    with tab_tolka:
        st.subheader("Tolka Division Standings")
        st.dataframe(
            style_league_table(tolka_df), 
            use_container_width=True, 
            hide_index=True
        )
        
        st.markdown("---")
        st.subheader("🏆 Tolka Division Results")
        if not results_df.empty and "Select your Box League Division" in results_df.columns:
            tolka_results = results_df[results_df["Select your Box League Division"].str.contains("Tolka", na=False)]
            if not tolka_results.empty:
                for _, row in tolka_results.iterrows():
                    winner = row.get("Winning Team", "")
                    loser = row.get("Losing Team", "")
                    w_score = row.get("Winning Team Score (Games won)", "")
                    l_score = row.get("Losing Team Score (Games won)", "")
                    date = row.get("Date of Match", "")
                    st.markdown(
                        f"""
                        <div class="result-card">
                            📅 <b>{date}</b> &nbsp;|&nbsp; 🏆 <b>{winner}</b> ({w_score}) vs. {loser} ({l_score})
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No results recorded for the Tolka Division yet.")
        else:
            st.info("No results recorded yet.")

    with tab_liffey:
            
        st.subheader("Liffey Division Standings")
        st.dataframe(
            style_league_table(liffey_df), 
            use_container_width=True, 
            hide_index=True,
        )
        
        st.markdown("---")
        st.subheader("🏆 Liffey Division Results")
        if not results_df.empty and "Select your Box League Division" in results_df.columns:
            liffey_results = results_df[results_df["Select your Box League Division"].str.contains("Liffey", na=False)]
            if not liffey_results.empty:
                for _, row in liffey_results.iterrows():
                    winner = row.get("Winning Team", "")
                    loser = row.get("Losing Team", "")
                    w_score = row.get("Winning Team Score (Games won)", "")
                    l_score = row.get("Losing Team Score (Games won)", "")
                    date = row.get("Date of Match", "")
                    st.markdown(
                        f"""
                        <div class="result-card">
                            📅 <b>{date}</b> &nbsp;|&nbsp; 🏆 <b>{winner}</b> ({w_score}) vs. {loser} ({l_score})
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No results recorded for the Liffey Division yet.")
        else:
            st.info("No results recorded yet.")

    with tab_rules:
        st.subheader("Charleville LTC Ladies Box League Rules")
        try:
            with open("rules.md", "r", encoding="utf-8") as f:
                rules_markdown = f.read()
            st.markdown(rules_markdown)
        except FileNotFoundError:            st.error("rules.md file not found. Please create it in your project root.")

except Exception as e:
    st.error(f"Could not load league tables: {e}")
    st.info("Ensure that your Google Sheet is shared with 'Anyone with the link can view'.")