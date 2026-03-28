import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Search", layout="centered")

st.title("🎓 Student Search System")

# ------------------ LOAD DATA ------------------ #
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    
    return df

df = load_data()

# ------------------ INPUT ------------------ #
query_params = st.query_params
search_param = query_params.get("id")

search_input = st.text_input("🔍 Search (ID / Name / Mobile / Hall / Floor)")

# ✅ Submit button
search_clicked = st.button("🔎 Search")

# Decide search value
search_value = None

if search_param:
    search_value = search_param[0].strip()
elif search_clicked and search_input:
    search_value = search_input.strip()

# ------------------ SEARCH ------------------ #
if search_value:
    result = df[df.apply(
        lambda row: row.astype(str).str.contains(search_value, case=False).any(),
        axis=1
    )]

    if not result.empty:
        st.success(f"✅ {len(result)} result(s) found")

        # 🎯 CARD VIEW DISPLAY
        for _, row in result.iterrows():
            with st.container():
                st.markdown("---")
                st.markdown(f"""
                ### 👤 {row.get('Name', '')}

                **🆔 Unique ID:** {row.get('Unique ID', '')}  
                **📱 Mobile:** {row.get('Mobile Number', '')}  
                **🏷 Category:** {row.get('Category', '')}  
                **🏫 Hall No:** {row.get('Hall No', '')}  
                **🏢 Floor:** {row.get('Floor', '')}  
                """)
    else:
        st.error("❌ No Data Found")

else:
    st.info("📌 QR scan செய்யவும் அல்லது value enter செய்து Search button அழுத்தவும்")
