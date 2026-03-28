import streamlit as st
import pandas as pd
import cv2
import numpy as np
from pyzbar.pyzbar import decode

st.set_page_config(page_title="Student Search", layout="centered")

st.title("POLLING OFFICER SEARCH SYSTEM")

# ------------------ DATA LOAD ------------------ #
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    
    return df

df = load_data()

# ------------------ SEARCH INPUT ------------------ #
st.subheader("🔍 Search")
search_input = st.text_input("Enter ID / Name / Mobile / Hall / Floor")

# ------------------ CAMERA QR SCAN ------------------ #
st.subheader("📷 Scan QR Code")
camera_image = st.camera_input("Scan QR Code using camera")

search_value = None

# QR decode
if camera_image is not None:
    file_bytes = np.asarray(bytearray(camera_image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    barcodes = decode(img)

    for barcode in barcodes:
        qr_data = barcode.data.decode("utf-8")
        st.success(f"QR Scanned: {qr_data}")
        search_value = qr_data

# Manual fallback
if search_input:
    search_value = search_input.strip()

# ------------------ SEARCH LOGIC ------------------ #
if search_value:
    result = df[df.apply(
        lambda row: row.astype(str).str.contains(search_value, case=False).any(),
        axis=1
    )]

    if not result.empty:
        st.success(f"✅ {len(result)} result(s) found")
        st.dataframe(result, use_container_width=True)
    else:
        st.error("❌ No Data Found")
else:
    st.info("📌 QR scan செய்யவும் அல்லது search value enter செய்யவும்")
