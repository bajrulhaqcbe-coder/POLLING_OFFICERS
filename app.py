import streamlit as st
import pandas as pd

st.set_page_config(page_title="Polling Officers Search", layout="centered")

st.title("🎓 Polling Officers Search System")

# ------------------ LOAD DATA ------------------ #
@st.cache_data
def load_data():
    df = pd.read_excel("2ND TRAINING ROOMS.xlsx")
    df.columns = df.columns.str.strip()

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    return df

df = load_data()

# ------------------ INPUT ------------------ #
query_params = st.query_params
search_param = query_params.get("id")

search_input = st.text_input("🔍 Search (ID / Name / Mobile / Hall / Floor)")
search_clicked = st.button("🔎 Search")

search_value = None

if search_param:
    search_value = search_param[0].strip()
elif search_clicked and search_input:
    search_value = search_input.strip()

# ------------------ SEARCH ------------------ #
if search_value:
    search_value = search_value.lower()

    mask = (
        df['Unique S.No'].str.lower().str.contains(search_value) |
        df['Name'].str.lower().str.contains(search_value) |
        df['Mobile Number'].str.contains(search_value) |
        df['Hall_no'].str.lower().str.contains(search_value) |
        df['Floor_No'].str.lower().str.contains(search_value) |
        df['TEAM_CODE'].str.lower().str.contains(search_value) |
        df['CATEGORY'].str.lower().str.contains(search_value)
    )

    result = df[mask]

    if not result.empty:
        st.success(f"✅ {len(result)} result(s) found")

        for _, row in result.iterrows():
            with st.container():
                st.markdown("---")
                st.markdown(f"""
                ### 👤 {row.get('Name', '')}

                **🆔 Unique No:** {row.get('Unique S.No', '')}  
                **📱 Mobile:** {row.get('Mobile Number', '')}  
                **🏷 Category:** {row.get('CATEGORY', '')}  
                **👥 Team Code:** {row.get('TEAM_CODE', '')}  
                **🎖 Designation:** {row.get('DESIGNATION', '')}  
                **🏫 Hall No:** {row.get('Hall_no', '')}  
                **🏢 Floor:** {row.get('Floor_No', '')}  
                """)

    else:
        st.error("❌ No Data Found")

else:
    st.info("📌 QR scan செய்யவும் அல்லது value enter செய்து Search button அழுத்தவும்")
