import streamlit as st
import pandas as pd
import io
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Polling Officers Search", layout="centered")

st.title("🎓 Polling Officers Search System")

# ------------------ LOAD DATA ------------------ #
@st.cache_data
def load_data():
    df = pd.read_excel("2ND TRAINING ROOMS.xlsx")

    # clean column names
    df.columns = df.columns.str.strip()

    # rename important columns
    df = df.rename(columns={
        "Unique S.No": "Unique_SNo",
        "Mobile Number": "Mobile_Number"
    })

    # clean values
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
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ]))

    content.append(table)

    doc.build(content)
    buffer.seek(0)
    return buffer


# ------------------ SEARCH ------------------ #
search_input = st.text_input("🔍 Search (ID / Name / Mobile / Hall / Floor)")

# ------------------ LOGIC ------------------ #
if search_input:

    search_value = search_input.strip().lower()
    search_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

        # ---------------- UPDATE ATTENDANCE WITH TIME ---------------- #
        for idx in result.index:
            df.at[idx, 'Attendance'] = f"Search @ {search_time}"

        # SAVE BACK TO EXCEL (IMPORTANT)
        df.to_excel("2ND TRAINING ROOMS.xlsx", index=False)

        # ---------------- SHOW TABLE ---------------- #
        st.subheader("📋 Attendance List")

        st.dataframe(result[[
            'Name',
            'Unique_SNo',
            'Mobile_Number',
            'CATEGORY',
            'TEAM_CODE',
            'Hall_no',
            'Floor_No',
            'Attendance'
        ]])

        # ---------------- DETAILS + PDF ---------------- #
        for _, row in result.iterrows():

            st.markdown("---")

            st.markdown(f"""
            ### 👤 {row['Name']}

            **🆔 Unique No:** {row['Unique_SNo']}  
            **📱 Mobile:** {row['Mobile_Number']}  
            **🏷 Category:** {row['CATEGORY']}  
            **👥 Team Code:** {row['TEAM_CODE']}  
            **🎖 Designation:** {row['DESIGNATION']}  
            **🏫 Hall No:** {row['Hall_no']}  
            **🏢 Floor:** {row['Floor_No']}  
            **📝 Attendance:** {row['Attendance']}
            """)

            pdf_buffer = create_pdf(row)

            st.download_button(
                label="📄 PDF Download",
                data=pdf_buffer,
                file_name=f"{row['Unique_SNo']}.pdf",
                mime="application/pdf"
            )

    else:
        st.error("❌ No Data Found")

else:
    st.info("📌 Search செய்து முடிவுகளை பார்க்கவும்")
