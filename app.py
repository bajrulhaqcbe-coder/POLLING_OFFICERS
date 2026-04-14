import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import io

st.set_page_config(page_title="Attendance System", layout="centered")

st.title("🎓 Attendance System")

# 🔥 YOUR GOOGLE SCRIPT URL
GOOGLE_SCRIPT_URL = "PASTE_YOUR_NEW_EXEC_URL_HERE"

# ---------------- DATA LOAD ---------------- #
@st.cache_data
def load_data():
    df = pd.read_excel("2ND TRAINING ROOMS.xlsx")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ---------------- GOOGLE SHEET LOG ---------------- #
def log_to_google_sheet(row):

    data = {
        "name": str(row.get('Name','')),
        "mobile": str(row.get('Mobile Number','')),
        "id": str(row.get('Unique S.No','')),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    response = requests.post(GOOGLE_SCRIPT_URL, json=data)

    st.write("STATUS CODE:", response.status_code)
    st.write("RESPONSE:", response.text)

# ---------------- SEARCH ---------------- #
search = st.text_input("🔍 Enter Mobile / ID")
btn = st.button("Search")

if btn and search:

    result = df[
        (df['Mobile Number'] == search) |
        (df['Unique S.No'].astype(str) == search)
    ]

    if not result.empty:

        for i, row in result.iterrows():

            st.markdown("---")

            st.write("👤 Name:", row['Name'])
            st.write("📱 Mobile:", row['Mobile Number'])
            st.write("🆔 ID:", row['Unique S.No'])

            # ✅ ATTENDANCE BUTTON
            if st.button("✅ Mark Attendance", key=f"btn_{i}"):

                log_to_google_sheet(row)
                st.success("Attendance Marked ✔")

    else:
        st.error("No Data Found")
