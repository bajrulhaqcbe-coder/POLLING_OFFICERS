import streamlit as st
import pandas as pd
import io
import base64

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

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
    animation_html = """
    <html>
    <head>
    <style>
    body { margin:0; overflow:hidden; }

    .gift {
        position: fixed;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 70px;
        animation: pop 1s ease-out forwards;
    }

    @keyframes pop {
        0% { transform: translate(-50%, -50%) scale(0); opacity:0; }
        100% { transform: translate(-50%, -50%) scale(1.2); opacity:1; }
    }
    </style>
    </head>

    <body>
        <div class="gift">🎁</div>

        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
        var duration = 2 * 1000;
        var end = Date.now() + duration;

        (function frame() {
          confetti({ particleCount: 6, angle: 60, spread: 60, origin: { x: 0 } });
          confetti({ particleCount: 6, angle: 120, spread: 60, origin: { x: 1 } });

          if (Date.now() < end) {
            requestAnimationFrame(frame);
          }
        }());
        </script>
    </body>
    </html>
    """

    st.components.v1.html(animation_html, height=200)

# ------------------ PDF FUNCTION ------------------ #
def create_pdf(row):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    # HEADER
    content.append(Paragraph("<b><font size=14>123 POLLACHI ASSEMBLY CONSTITUENCY</font></b>", styles['Title']))
    content.append(Spacer(1, 8))
    content.append(Paragraph("<b>சட்ட மன்ற தேர்தல்-2026</b>", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph(
        "<b>Training Center:</b><br/>"
        "டாக்டர். மஹாலிங்காம் பொறியியல் மற்றும் தொழில்நுட்பக் கல்லூரி (எம்.சி.இ.டி)",
        styles['Normal']
    ))

    content.append(Spacer(1, 20))

    # TABLE
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
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (0,-1), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
    ]))

    content.append(table)

    doc.build(content)

    buffer.seek(0)
    return buffer

# ------------------ AUTO DOWNLOAD ------------------ #
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
        show_gift_animation()  # 🎁 Animation
        st.success(f"✅ {len(result)} result(s) found")

        # TITLE CARD
        st.markdown("""
        <div style="text-align:center; padding:10px; border:2px solid black; border-radius:10px; margin-bottom:20px;">
            <h3>123 POLLACHI ASSEMBLY CONSTITUENCY</h3>
            <h4>Tamil Nadu Legislative Assembly election</h4>
            <p><b>Training Center:</b><br>
            Dr. Mahalingam College of Engineering and Technology (MCET))</p>
        </div>
        """, unsafe_allow_html=True)

            # RESULT DISPLAY
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
    st.info("📌 QR scan செய்யவும் அல்லது value enter செய்து Search button அழுத்தவும்")
