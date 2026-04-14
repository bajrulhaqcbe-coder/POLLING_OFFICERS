import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="Polling Officers Search", layout="centered")
st.title("🎓 Polling Officers Search System")

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyhioXYQu4uts0mlLBvv7kB3XiPuWlm6lDjiR4a8Yjh1PSYHgN2l5RrEtgcvgg3SWZH/exec"

# ---------------- LOAD DATA ---------------- #
df = pd.read_excel("2ND TRAINING ROOMS.xlsx")

# clean columns (VERY IMPORTANT FIX)
df.columns = df.columns.str.strip()

# optional safe rename (space remove)
df.columns = df.columns.str.replace(" ", "_")

# ---------------- API FUNCTION ---------------- #
def update_google_sheet(unique_no):

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "Unique_SNo": unique_no,
        "Time": time
    }

    try:
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=5)
    except:
        pass

# ---------------- SEARCH ---------------- #
search_input = st.text_input("🔍 Search (ID / Name / Mobile / Hall / Floor)")

if search_input:

    search_value = search_input.strip().lower()

    mask = (
        df['Unique_S.No'].astype(str).str.lower().str.contains(search_value) |
        df['Name'].astype(str).str.lower().str.contains(search_value) |
        df['Mobile_Number'].astype(str).str.contains(search_value) |
        df['Hall_no'].astype(str).str.lower().str.contains(search_value) |
        df['Floor_No'].astype(str).str.lower().str.contains(search_value) |
        df['TEAM_CODE'].astype(str).str.lower().str.contains(search_value) |
        df['CATEGORY'].astype(str).str.lower().str.contains(search_value)
    )

    result = df[mask]

    if not result.empty:

        st.success(f"✅ {len(result)} result(s) found")

        # ---------------- UPDATE GOOGLE SHEET ---------------- #
        for _, row in result.iterrows():
            update_google_sheet(row['Unique_S.No'])

        # ---------------- DISPLAY ---------------- #
        st.dataframe(result[[
            'S.No',
            'Unique_S.No',
            'CATEGORY',
            'TEAM_CODE',
            'Name',
            'Mobile_Number',
            'DESIGNATION',
            'Hall_no',
            'Floor_No',
            'Entry_time',
            'Attendance'
        ]])

    else:
        st.error("❌ No Data Found")

else:
    st.info("📌 Search செய்து முடிவுகளை பார்க்கவும்")
