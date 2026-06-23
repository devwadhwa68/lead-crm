import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os
import json
import base64
import pandas as pd
import plotly.express as px
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

st.set_page_config(page_title="CRM Dashboard", page_icon="📊", layout="wide")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = "15l2G3kwcZq1rZEvOj4rHsOy-L-F38CzXsIE1VMvobzY"

def get_sheet():
    creds_json = base64.b64decode(st.secrets["GOOGLE_CREDS_B64"]).decode('utf-8')
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1

@st.cache_data(ttl=60)
def load_data():
    sheet = get_sheet()
    data = sheet.get_all_records()
    return pd.DataFrame(data)

st.title("📊 AI Lead CRM Dashboard")
st.caption("Real-time lead tracking with AI scoring")

df = load_data()

if df.empty:
    st.warning("No leads yet. Submit some inquiries first!")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", len(df))
    with col2:
        hot = len(df[df['Status'] == 'Hot']) if 'Status' in df.columns else 0
        st.metric("🔥 Hot Leads", hot)
    with col3:
        warm = len(df[df['Status'] == 'Warm']) if 'Status' in df.columns else 0
        st.metric("🌡️ Warm Leads", warm)
    with col4:
        cold = len(df[df['Status'] == 'Cold']) if 'Status' in df.columns else 0
        st.metric("❄️ Cold Leads", cold)

    st.divider()

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Lead Distribution")
        if 'Status' in df.columns:
            status_counts = df['Status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']
            colors = {'Hot': '#E74C3C', 'Warm': '#F39C12', 'Cold': '#3498DB'}
            fig = px.pie(status_counts, values='Count', names='Status',
                        color='Status', color_discrete_map=colors)
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("All Leads")
        filter_status = st.selectbox("Filter by status:", ["All", "Hot", "Warm", "Cold"])
        if filter_status != "All":
            filtered_df = df[df['Status'] == filter_status]
        else:
            filtered_df = df
        st.dataframe(filtered_df, use_container_width=True)

    st.divider()
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()