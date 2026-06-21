import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

os.environ["GROQ_API_KEY"] = "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"

st.set_page_config(page_title="AI Lead Capture", page_icon="📋")
st.title("📋 Submit Your Inquiry")
st.caption("Powered by AI — your inquiry will be reviewed instantly")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
client = gspread.authorize(creds)
SHEET_ID = "15l2G3kwcZq1rZEvOj4rHsOy-L-F38CzXsIE1VMvobzY"
sheet = client.open_by_key(SHEET_ID).sheet1

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def score_lead(name, email, company, message):
    prompt = f"""Score this lead from 1-10 and classify as Hot/Warm/Cold.
Name: {name}
Email: {email}
Company: {company}
Message: {message}

Reply in this exact format only:
Score: X/10
Status: Hot/Warm/Cold
Reason: one line reason"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

with st.form("lead_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Email")
    company = st.text_input("Company (optional)")
    message = st.text_area("What are you looking for?")
    submitted = st.form_submit_button("Submit Inquiry")

if submitted:
    if name and email and message:
        with st.spinner("Processing your inquiry..."):
            ai_response = score_lead(name, email, company, message)
            lines = ai_response.strip().split('\n')
            score = lines[0].replace('Score: ', '')
            status = lines[1].replace('Status: ', '')
            sheet.append_row([name, email, company, message, score, status])
        st.success("Thank you! We've received your inquiry and will get back to you shortly.")
    else:
        st.error("Please fill in your name, email, and message.")