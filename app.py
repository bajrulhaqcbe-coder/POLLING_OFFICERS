import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Search", layout="centered")

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Search", layout="centered")

st.title("123 POLLACHI AC TRAINING-2")
st.title("🎓 Polling Officer Search System")
@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    
    return df

df = load_data()

query_params = st.query_params
search_param = query_params.get("id")

search_input = st.text_input("🔍 Search (ID / Name / Mobile / Hall...)")

if search_param:
    search_value = search_param[0].strip()
elif search_input:
    search_value = search_input.strip()
else:
    search_value = None

if search_value:
    result = df[df.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    if not result.empty:
        st.success(f"✅ {len(result)} result(s) found")
        st.dataframe(result, use_container_width=True)
    else:
        st.error("❌ No Data Found")
else:
    st.info("📌 QR scan செய்யவும் அல்லது search value type செய்யவும்")

@st.cache_data
def load_data():
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    
    return df

df = load_data()

query_params = st.query_params
search_param = query_params.get("id")

search_input = st.text_input("🔍 Search (ID / Name / Mobile / Hall...)")

if search_param:
    search_value = search_param[0].strip()
elif search_input:
    search_value = search_input.strip()
else:
    search_value = None

if search_value:
    result = df[df.apply(lambda row: row.astype(str).str.contains(search_value, case=False).any(), axis=1)]

    if not result.empty:
        st.success(f"✅ {len(result)} result(s) found")
        st.dataframe(result, use_container_width=True)
    else:
        st.error("❌ No Data Found")
else:
    st.info("📌 QR scan செய்யவும் அல்லது search value type செய்யவும்")
