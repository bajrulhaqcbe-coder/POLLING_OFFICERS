import streamlit as st
import pandas as pd
import io
import requests
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Polling Attendance System", layout="centered")

st.title("🎓 Polling Attendance System")

# ------------------ CONFIG ------------------ #
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2qjXpBHy8K56TT0X7mFEkd1IM7hteQ5nBGEg_LJRSu7jUOvjQOmuDriZyBC3aObl8BQ/exec"

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vShNwIU6UuvbAWenZN4TYQX3kDf8fB0m7TybDc5P7pqEpnKP--xGT1Cb3ITXnGgEbOOgVzOeVcmSi_P/pub?output=csv"

# ------------------ LOAD EXCEL ------------------ #
@st.cache_data
def load_data():
    df = pd.read_excel("2ND TRAINING ROOMS.xlsx")
    df.columns = df.columns.str.strip()

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    return df

df = load_data()

# ------------------ PDF FUNCTION ------------------ #
def create_pdf(row):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b><font size=14>123 POLLACHI ASSEMBLY CONSTITUENCY</font></b>", styles['Title']))
    content.append(Spacer(1, 10))

    data = [
        ["Field", "Details"],
        ["Name", row.get('Name','')],
        ["Unique No", row.get('Unique S.No','')],
        ["Mobile", row.get('Mobile Number','')],
        ["Hall", row.get('Hall_no','')],
        ["Floor", row.get('Floor_No','')],
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ]))

    content.append(table)
    doc.build(content)

    buffer.seek(0)
    return buffer

# ------------------ GOOGLE SHEET LOG ------------------ #
def log_to_google_sheet(row):
    data = {
        "name": row.get('Name',''),
        "mobile": row.get('Mobile Number',''),
        "id": row.get('Unique S.No',''),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        requests.post(GOOGLE_SCRIPT_URL, json=data)
    except:
        st.error("❌ Logging Failed")

# ------------------ DASHBOARD ------------------ #
@st.cache_data(ttl=5)
def load_dashboard():
    dash_df = pd.read_csv(SHEET_CSV_URL)

    # Clean columns
    dash_df.columns = dash_df.columns.str.strip()

    # Clean Status
    dash_df['Status'] = dash_df['Status'].astype(str).str.strip().str.lower()

    return dash_df

try:
    dash_df = load_dashboard()

    total = len(dash_df)
    present = len(dash_df[dash_df['Status'] == 'present'])
    duplicate = len(dash_df[dash_df['Status'] == 'duplicate'])

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total", total)
    col2.metric("✅ Present", present)
    col3.metric("⚠️ Duplicate", duplicate)

    # Debug (optional remove later)
    # st.write(dash_df.head())
    # st.write(dash_df['Status'].unique())

except Exception as e:
    st.error(f"Dashboard Error: {e}")

# ------------------ SEARCH ------------------ #
search = st.text_input("🔍 Enter Mobile Number or Unique ID")
btn = st.button("Search")

if btn and search:
    search = search.strip()

    result = df[
        (df['Mobile Number'] == search) |
        (df['Unique S.No'].str.lower() == search.lower())
    ]

    if not result.empty:
        st.success("✅ Record Found")

        for i, row in result.iterrows():

            st.markdown("---")

            st.markdown(f"""
            ### 👤 {row.get('Name','')}
            **🆔 Unique ID:** {row.get('Unique S.No','')}  
            **📱 Mobile:** {row.get('Mobile Number','')}  
            **🏫 Hall:** {row.get('Hall_no','')}  
            **🏢 Floor:** {row.get('Floor_No','')}  
            """)

            # Attendance Button
            if st.button(f"✅ Mark Attendance {i}"):
                log_to_google_sheet(row)
                st.success("Attendance Marked Successfully")

            # PDF Download
            pdf_buffer = create_pdf(row)

            st.download_button(
                label="📄 Download PDF",
                data=pdf_buffer,
                file_name=f"{row.get('Unique S.No','result')}.pdf",
                mime="application/pdf"
            )

    else:
        st.error("❌ No Data Found")
