import streamlit as st
import pandas as pd
import io
import base64

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Polling Officers Search", layout="centered")

st.title("🎓 Polling Officers Search System")

# ------------------ LOAD DATA ------------------ #
@st.cache_data
def load_data():
    df = pd.read_excel("2ND TRAINING ROOMS.xlsx")

    # Column clean
    df.columns = df.columns.str.strip()

    # Value clean
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

    content.append(Paragraph(f"<b>Name:</b> {row.get('Name','')}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Unique No:</b> {row.get('Unique S.No','')}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Mobile:</b> {row.get('Mobile Number','')}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Category:</b> {row.get('CATEGORY','')}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Team Code:</b> {row.get('TEAM_CODE','')}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Designation:</b> {row.get('DESIGNATION','')}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Hall No:</b> {row.get('Hall_no','')}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"<b>Floor:</b> {row.get('Floor_No','')}", styles['Normal']))

    doc.build(content)

    buffer.seek(0)
    return buffer


# ------------------ AUTO DOWNLOAD FUNCTION ------------------ #
def auto_download_pdf(pdf_buffer, filename="result.pdf"):
    b64 = base64.b64encode(pdf_buffer.getvalue()).decode()

    html = f"""
    <html>
    <body>
    <a id="download" href="data:application/pdf;base64,{b64}" download="{filename}"></a>
    <script>
        document.getElementById('download').click();
    </script>
    </body>
    </html>
    """

    st.components.v1.html(html, height=0)


# ------------------ INPUT ------------------ #
query_params = st.query_params
search_param = query_params.get("id")

search_input = st.text_input("🔍 Search (ID / Name / Mobile / Hall / Floor)")
search_clicked = st.button("🔎 Search")

search_value = None

if search_param:
    search_value = search_param[0].strip()
elif search_clicked and search_input:
    search_value = search_input.strip()

# ------------------ SEARCH ------------------ #
if search_value:
    search_value = search_value.lower()

    mask = (
        df['Unique S.No'].str.lower().str.contains(search_value) |
        df['Name'].str.lower().str.contains(search_value) |
        df['Mobile Number'].str.contains(search_value) |
        df['Hall_no'].str.lower().str.contains(search_value) |
        df['Floor_No'].str.lower().str.contains(search_value) |
        df['TEAM_CODE'].str.lower().str.contains(search_value) |
        df['CATEGORY'].str.lower().str.contains(search_value)
    )

    result = df[mask]

    if not result.empty:
        st.balloons()  # 🎉 animation
        st.success(f"✅ {len(result)} result(s) found")

        # 👉 FIRST RESULT மட்டும் auto download (browser block avoid)
        first_row = result.iloc[0]
        pdf_buffer = create_pdf(first_row)

        auto_download_pdf(
            pdf_buffer,
            filename=f"{first_row.get('Unique S.No','result')}.pdf"
        )

        # 👉 Result display
        for _, row in result.iterrows():
            with st.container():
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

    else:
        st.error("❌ No Data Found")

else:
    st.info("📌 QR scan செய்யவும் அல்லது value enter செய்து Search button அழுத்தவும்")
