import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import io

st.set_page_config(page_title="Attendance System", layout="centered")

st.title("🎓 Attendance System")

# 🔥 YOUR GOOGLE SCRIPT URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyVi6aqOzEUOqQwoQCeGBx0LhSkBpKbdQZ6b-_XpOa5rmJJ_Ef4onWpqJ0O88Xtnrjy8g/exec"

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

    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json=data,
            headers={"Content-Type": "application/json"}
        )

        st.write("STATUS CODE:", response.status_code)
        st.write("RESPONSE TEXT:", response.text)

    except Exception as e:
        st.error(e)
# ---------------- SEARCH ---------------- #
search = st.text_input("🔍 Enter Mobile / ID")

btn = st.button("Search")

if btn and search:

    search = search.strip()

    df.columns = df.columns.str.strip()

    # 🔥 CLEAN DATA (IMPORTANT)
    df['Mobile Number'] = df['Mobile Number'].astype(str).str.strip()
    df['Unique S.No'] = df['Unique S.No'].astype(str).str.strip()

    result = df[
        (df['Mobile Number'] == search) |
        (df['Unique S.No'] == search)
    ]

    if len(result) > 0:

        for i, row in result.iterrows():

            st.success("✅ Found")

            st.write("👤 Name:", row['Name'])
            st.write("📱 Mobile:", row['Mobile Number'])
           if st.button("Mark Attendance", key=f"att_{i}"):

    st.write("Sending data...")

    log_to_google_sheet(row)

    st.success("Attendance Marked ✔")
    else:
        st.error("❌ No Data Found")
