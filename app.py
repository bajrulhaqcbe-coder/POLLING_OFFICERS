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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

def create_pdf(row):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    # 🎯 TITLE
    content.append(Paragraph("<b><font size=14>Polling Officers Details</font></b>", styles['Title']))
    content.append(Spacer(1, 20))

    # 🎯 TABLE DATA (Card Style)
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

    # 🎨 STYLE
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),

        ("ALIGN", (0,0), (-1,-1), "LEFT"),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey]),
    ]))

    content.append(table)

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
