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
    df = pd.read_excel("output.xlsx")

    df.columns = df.columns.str.strip()

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    return df

df = load_data()

# ------------------ GIFT ANIMATION ------------------ #
def show_gift_animation():
    animation_html = """<div style="text-align:center;font-size:60px;">🎁</div>"""
    st.components.v1.html(animation_html, height=150)

# ------------------ PDF FUNCTION ------------------ #
def create_pdf(row):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b><font size=14>123 POLLACHI ASSEMBLY CONSTITUENCY</font></b>", styles['Title']))
    content.append(Spacer(1, 8))
    content.append(Paragraph("<b>Tamil Nadu Legislative Assembly election</b>", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "<b>Training Center:</b><br/>"
        "Dr. Mahalingam College of Engineering and Technology (MCET)",
        styles['Normal']
    ))

    content.append(Spacer(1, 20))

    # 🔴 PDF ல Hall No NORMAL தான்
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
        show_gift_animation()
        st.success(f"✅ {len(result)} result(s) found")

            # RESULT LOOP
        for _, row in result.iterrows():
            with st.container():
                st.markdown("---")
# TITLE CARD
        st.markdown("""
        <div style="text-align:center; padding:10px; border:2px solid black; border-radius:10px; margin-bottom:20px;">
            <h3>123 POLLACHI ASSEMBLY CONSTITUENCY</h3>
            <h4>Tamil Nadu Legislative Assembly election</h4>
            <p><b>Training Center:</b><br>
            Dr. Mahalingam College of Engineering and Technology (MCET)</p>
        </div>
        """, unsafe_allow_html=True)
                st.markdown(f"""
                ### 👤 {row.get('Name', '')}

    **🏫** <span style="font-size:70px; font-weight:bold; color:red;">
                {row.get('Hall_no', '')}
                </span>  
                **🆔 Unique No:** {row.get('Unique S.No', '')}  
                **📱 Mobile:** {row.get('Mobile Number', '')}  
                **🏷 Category:** {row.get('CATEGORY', '')}  
                **👥 Team Code:** {row.get('TEAM_CODE', '')}  
                **🎖 Designation:** {row.get('DESIGNATION', '')}  
               **🏢 Floor:** {row.get('Floor_No', '')}  
                """, unsafe_allow_html=True)
    
                pdf_buffer = create_pdf(row)

                st.download_button(
                    label="📄 PDF Download",
                    data=pdf_buffer,
                    file_name=f"{row.get('Unique S.No','result')}.pdf",
                    mime="application/pdf"
                )

    else:
        st.error("❌ No Data Found")

else:
    st.info("📌 Mobile / Unique ID / Name / Hall No இவற்றில் ஏதேனும் ஒன்றை Enter செய்து Search செய்யவும்")
