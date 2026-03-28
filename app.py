import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Search", layout="centered")

st.title("123 POLLACHI ASSEMBLY CONSTITUENCY TRAINING-2")
st.title("POLLING OFFICER SEARCH SYSTEM")
# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")
    
    # Column clean
    df.columns = df.columns.str.strip()
    
    # அனைத்து columns-யும் string ஆக மாற்றம்
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    
    return df

df = load_data()

# URL parameter
query_params = st.query_params
search_param = query_params.get("id")

# Manual input
search_input = st.text_input("🔍 எந்த value வேண்டுமானாலும் type செய்யவும்")

# Final search value
if search_param:
    search_value = search_param[0].strip()
elif search_input:
    search_value = search_input.strip()
else:
    search_value = None

# 🔥 MAIN SEARCH LOGIC (ANY COLUMN)
if search_value:
    # அனைத்து columns-லும் search
    result = df[df.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    if not result.empty:
        st.success(f"✅ {len(result)} result(s) found")
        st.dataframe(result, use_container_width=True)
    else:
        st.error("❌ No Data Found")
else:
    st.info("📌 QR scan செய்யவும் அல்லது search value type செய்யவும்")

# Debug (optional)
with st.expander("⚙ Debug"):
    st.write("Columns:", df.columns.tolist())
    st.dataframe(df.head())