import streamlit as st
import pandas as pd
import io
import requests
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Polling Officers Search", layout="centered")

st.title("🎓 Polling Officers Search System")

# ------------------ CONFIG ------------------ #
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2qjXpBHy8K56TT0X7mFEkd1IM7hteQ5nBGEg_LJRSu7jUOvjQOmuDriZyBC3aObl8BQ/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vShNwIU6UuvbAWenZN4TYQX3kDf8fB0m7TybDc5P7pqEpnKP--xGT1Cb3ITXnGgEbOOgVzOeVcmSi_P/pub?output=csv"

# ------------------ LOAD DATA ------------------ #
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
    content.append(Spacer(1, 8))
    content.append(Paragraph("<b>Tamil Nadu Legislative Assembly election-2026</b>", styles['Title']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "<b>Training Center:</b><br/>Dr. Mahalingam College of Engineering and Technology (MCET)",
        styles['Normal']
    ))

    content.append(Spacer(1, 20))

    data = [
        ["Field", "Details"],
        ["Name", row.get('Name','')],
        ["Unique No", row.get('Unique S.No','')],
        ["Mobile", row.get('Mobile Number','')],
        ["Category", row.get('CATEGORY','')],
        ["Team Code", row.get('TEAM_CODE','')],
        ["Designation", row.get('DESIGNATION','')],
        ["Hall No", row.get('Hall_no','')],
        ["Floor", row.get('Floor_No','')],
    ]

    table = Table(data, colWidths=[120, 250])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ]))

    content.append(table)

    doc.build(content)
    buffer.seek(0)
    return buffer

# ------------------ GOOGLE SHEET LOG ------------------ #
def log_to_google_sheet(row):
    data = {
        "name": row.get('Name', ''),
        "mobile": row.get('Mobile Number', ''),
        "id": row.get('Unique S.No', ''),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        requests.post("https://script.google.com/macros/s/AKfycbz2qjXpBHy8K56TT0X7mFEkd1IM7hteQ5nBGEg_LJRSu7jUOvjQOmuDriZyBC3aObl8BQ/exec, json=data")
    except:
        pass

# ------------------ DASHBOARD ------------------ #
@st.cache_data(ttl=5)
def load_dashboard():
    return pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vShNwIU6UuvbAWenZN4TYQX3kDf8fB0m7TybDc5P7pqEpnKP--xGT1Cb3ITXnGgEbOOgVzOeVcmSi_P/pub?output=csv")

try:
    dash_df = load_dashboard()

    total = len(dash_df)
    present = len(dash_df[dash_df['Status'] == 'Present'])
    duplicate = len(dash_df[dash_df['Status'] == 'Duplicate'])

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total", total)
    col2.metric("✅ Present", present)
    col3.metric("⚠️ Duplicate", duplicate)

except:
    st.warning("Dashboard not loaded")

# ------------------ SEARCH ------------------ #
search_input = st.text_input("🔍 Enter Mobile Number or Unique ID")
search_clicked = st.button("🔎 Search")

if search_clicked and search_input:

    search_value = search_input.strip()

    mask = (
        (df['Mobile Number'] == search_value) |
        (df['Unique S.No'].str.lower() == search_value.lower())
    )

    result = df[mask]

    if not result.empty:
        st.success(f"✅ {len(result)} result(s) found")

        for i, row in result.iterrows():

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

            # 🔥 Attendance Button
            if st.button(f"✅ Mark Attendance - {i}"):

                log_to_google_sheet(row)
                st.success("Attendance Marked!")

            # PDF
            pdf_buffer = create_pdf(row)

            st.download_button(
                label="📄 PDF Download",
                data=pdf_buffer,
                file_name=f"{row.get('Unique S.No','result')}.pdf",
                mime="application/pdf"
            )

    else:
        st.error("❌ No Data Found")
