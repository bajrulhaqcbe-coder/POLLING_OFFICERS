import streamlit as st
import pandas as pd
import io

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Polling Officers Search", layout="centered")

st.title("🎓 Polling Officers Search System")

# ------------------ LOAD DATA ------------------ #
@st.cache_data
def load_data():
    df = pd.read_excel("2ND TRAINING ROOMS.xlsx")

    # Clean column names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(" ", "_")

    # Clean data
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

    content.append(Paragraph("123 POLLACHI ASSEMBLY CONSTITUENCY", styles['Title']))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Training Center: MCET College", styles['Normal']))
    content.append(Spacer(1, 20))

    data = [
        ["Field", "Details"],
        ["Name", row.get('Name','')],
        ["Unique No", row.get('Unique_SNo','')],
        ["Mobile", row.get('Mobile_Number','')],
        ["Category", row.get('CATEGORY','')],
        ["Team Code", row.get('TEAM_CODE','')],
        ["Designation", row.get('DESIGNATION','')],
        ["Hall No", row.get('Hall_no','')],
        ["Floor", row.get('Floor_No','')],
        ["Attendance", row.get('Attendance','Not Marked')],
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

# ------------------ SEARCH INPUT ------------------ #
search_input = st.text_input("🔍 Search (ID / Name / Mobile / Hall / Floor)")
search_clicked = st.button("🔎 Search")

search_value = None

if search_clicked and search_input:
    search_value = search_input.strip().lower()

# ------------------ SEARCH LOGIC ------------------ #
if search_value:

    mask = (
        df['Unique_SNo'].str.lower().str.contains(search_value) |
        df['Name'].str.lower().str.contains(search_value) |
        df['Mobile_Number'].str.contains(search_value) |
        df['Hall_no'].str.lower().str.contains(search_value) |
        df['Floor_No'].str.lower().str.contains(search_value) |
        df['TEAM_CODE'].str.lower().str.contains(search_value) |
        df['CATEGORY'].str.lower().str.contains(search_value)
    )

    result = df[mask]

    if not result.empty:

        st.success(f"✅ {len(result)} result(s) found")

        # ------------------ ATTENDANCE TABLE ------------------ #
        st.subheader("📋 Attendance List")

        cols_to_show = ['Name','Unique_SNo','Hall_no','Floor_No','Attendance']
        existing_cols = [c for c in cols_to_show if c in result.columns]

        st.dataframe(result[existing_cols])

        # ------------------ DETAILS ------------------ #
        for _, row in result.iterrows():

            st.markdown("---")

            st.markdown(f"""
            ### 👤 {row.get('Name', '')}

            **🆔 Unique No:** {row.get('Unique_SNo', '')}  
            **📱 Mobile:** {row.get('Mobile_Number', '')}  
            **🏷 Category:** {row.get('CATEGORY', '')}  
            **👥 Team Code:** {row.get('TEAM_CODE', '')}  
            **🎖 Designation:** {row.get('DESIGNATION', '')}  
            **🏫 Hall No:** {row.get('Hall_no', '')}  
            **🏢 Floor:** {row.get('Floor_No', '')}  
            **📝 Attendance:** {row.get('Attendance','Not Marked')}
            """)

            pdf_buffer = create_pdf(row)

            st.download_button(
                label="📄 PDF Download",
                data=pdf_buffer,
                file_name=f"{row.get('Unique_SNo','result')}.pdf",
                mime="application/pdf"
            )

    else:
        st.error("❌ No Data Found")

else:
    st.info("📌 Search செய்து முடிவுகளை பார்க்கவும்")
