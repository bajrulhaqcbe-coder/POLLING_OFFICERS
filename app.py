import streamlit as st
import pandas as pd
import io

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Tamil Font Register
pdfmetrics.registerFont(TTFont('TamilFont', 'NotoSansTamil.ttf'))

st.set_page_config(page_title="Polling Officers Search", layout="centered")

st.title("🎓 Polling Officers Search System")

# ------------------ LOAD DATA ------------------ #
@st.cache_data
def load_data():
    df = pd.read_excel("2ND TRAINING ROOMS.xlsx")
    df.columns = df.columns.str.strip()

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    return df

df = load_data()

# ------------------ GIFT ANIMATION ------------------ #
def show_gift_animation():
    st.markdown("## 🎁 Results Ready!")

# ------------------ PDF FUNCTION ------------------ #
def create_pdf(row):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    tamil_style = styles['Normal']
    tamil_style.fontName = 'TamilFont'
    tamil_style.fontSize = 11

    content = []

    content.append(Paragraph("123 POLLACHI ASSEMBLY CONSTITUENCY", tamil_style))
    content.append(Spacer(1, 8))
    content.append(Paragraph("சட்ட மன்ற தேர்தல்-2026", tamil_style))
    content.append(Spacer(1, 10))
    content.append(Paragraph(
        "Training Center:<br/>"
        "டாக்டர். மஹாலிங்காம் பொறியியல் மற்றும் தொழில்நுட்பக் கல்லூரி (எம்.சி.இ.டி)",
        tamil_style
    ))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"பெயர்: {row.get('Name','')}", tamil_style))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"Unique No: {row.get('Unique S.No','')}", tamil_style))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"Mobile: {row.get('Mobile Number','')}", tamil_style))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"Hall No: {row.get('Hall_no','')}", tamil_style))
    content.append(Spacer(1, 5))
    content.append(Paragraph(f"Floor: {row.get('Floor_No','')}", tamil_style))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ------------------ INPUT ------------------ #
search_input = st.text_input("🔍 Search (ID / Name / Mobile / Hall / Floor)")
search_clicked = st.button("🔎 Search")

# ------------------ SEARCH ------------------ #
if search_clicked and search_input:
    search_value = search_input.strip().lower()

    mask = (
        df['Unique S.No'].str.lower().str.contains(search_value) |
        df['Name'].str.lower().str.contains(search_value) |
        df['Mobile Number'].str.contains(search_value) |
        df['Hall_no'].str.lower().str.contains(search_value) |
        df['Floor_No'].str.lower().str.contains(search_value)
    )

    result = df[mask]

    if not result.empty:
        show_gift_animation()
        st.success(f"✅ {len(result)} result(s) found")

        # TITLE CARD
        st.markdown("""
        <div style="text-align:center; padding:10px; border:2px solid black; border-radius:10px;">
            <h3>123 POLLACHI ASSEMBLY CONSTITUENCY</h3>
            <h4>சட்ட மன்ற தேர்தல்-2026</h4>
            <p><b>Training Center:</b><br>
            டாக்டர். மஹாலிங்காம் பொறியியல் மற்றும் தொழில்நுட்பக் கல்லூரி (எம்.சி.இ.டி)</p>
        </div>
        """, unsafe_allow_html=True)

        for _, row in result.iterrows():
            st.markdown("---")

            st.markdown(f"""
            ### 👤 {row.get('Name', '')}

            🆔 {row.get('Unique S.No', '')}  
            📱 {row.get('Mobile Number', '')}  
            🏫 Hall: {row.get('Hall_no', '')}  
            🏢 Floor: {row.get('Floor_No', '')}  
            """)

            # 👉 PDF create
            pdf_buffer = create_pdf(row)

            # 👉 DOWNLOAD BUTTON
            st.download_button(
                label="📄 PDF Download",
                data=pdf_buffer,
                file_name=f"{row.get('Unique S.No','result')}.pdf",
                mime="application/pdf"
            )

    else:
        st.error("❌ No Data Found")

else:
    st.info("📌 value enter செய்து Search button அழுத்தவும்")
