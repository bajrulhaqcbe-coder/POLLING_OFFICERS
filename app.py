import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ---------------- APP CONFIG ---------------- #
st.set_page_config(page_title="Polling Officers Search", layout="centered")
st.title("🎓 Polling Officers Search System")

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx7WiyONghLCJOdwG4F66IY40GM42RNF00kYxbaXFGaWPQ4CeqUat5zTnGY91spH0Yc/exec"

# ---------------- LOAD DATA ---------------- #
df = pd.read_excel("2ND TRAINING ROOMS.xlsx")

# CLEAN COLUMNS
df.columns = df.columns.str.strip()

# 🔥 FIX: CLEAN ALL COLUMN NAMES PROPERLY
df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace(".", "_")
)

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

# ---------------- SEARCH INPUT ---------------- #
search_input = st.text_input("🔍 Search (ID / Name / Mobile / Hall / Floor)")

if search_input:

    search_value = search_input.strip().lower()

    mask = (
        df['Unique_S_No'].astype(str).str.lower().str.contains(search_value) |
        df['Name'].astype(str).str.lower().str.contains(search_value) |
        df['Mobile_Number'].astype(str).str.contains(search_value)
    )

    result = df[mask]

    if not result.empty:
        st.success("Found")
        st.dataframe(result)
        # 🔥 UPDATE GOOGLE SHEET
        for _, row in result.iterrows():
            update_google_sheet(row['Unique_S_No'])

        # ---------------- DISPLAY TABLE ---------------- #
        st.dataframe(result[[
    'Unique_S_No',
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
