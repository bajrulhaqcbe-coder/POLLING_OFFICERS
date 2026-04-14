import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Polling Officers Search", layout="centered")
st.title("🎓 Polling Officers Search System")

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby23u0l0QbailYnsSluJ_9nSxRn1onjDflNSd-zuymNLfEtS32dfAueRWSoIWsAsiLL/exec"

# ---------------- LOAD DATA ---------------- #
df = pd.read_excel("2ND TRAINING ROOMS.xlsx")

df.columns = df.columns.str.strip()

df = df.rename(columns={
    "Unique S.No": "Unique_SNo",
    "Mobile_Number": "Mobile_Number"
})

for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# ---------------- API FUNCTION ---------------- #
def update_google_sheet(unique_no):

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "Unique_SNo": unique_no,
        "Time": time
    }

    try:
        requests.post(GOOGLE_SCRIPT_URL, json=payload)
    except:
        pass

# ---------------- SEARCH ---------------- #
search_input = st.text_input("🔍 Search")

if search_input:

    search_value = search_input.strip().lower()

    mask = (
        df['Unique_SNo'].fillna('').str.lower().str.contains(search_value) |
        df['Name'].fillna('').str.lower().str.contains(search_value) |
        df['Mobile_Number'].astype(str).str.contains(search_value) |
        df['Hall_no'].fillna('').str.lower().str.contains(search_value) |
        df['Floor_No'].fillna('').str.lower().str.contains(search_value) |
        df['TEAM_CODE'].fillna('').str.lower().str.contains(search_value) |
        df['CATEGORY'].fillna('').str.lower().str.contains(search_value)
    )

    result = df[mask]

    if not result.empty:

        st.success(f"✅ {len(result)} result(s) found")

        # 🔥 UPDATE GOOGLE SHEET (Entry_time + Attendance)
        for _, row in result.iterrows():
            update_google_sheet(row['Unique_SNo'])

        st.dataframe(result[[
            'S.No',
            'Unique_SNo',
            'CATEGORY',
            'TEAM_CODE',
            'Name',
            'Mobile_Number',
            'DESIGNATION',
            'Hall_no',
            'Floor_No'
        ]])

    else:
        st.error("❌ No Data Found")

else:
    st.info("📌 Search செய்து முடிவுகளை பார்க்கவும்")
