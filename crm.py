import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

# Google Sheets connect karo
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_ID = "15l2G3kwcZq1rZEvOj4rHsOy-L-F38CzXsIE1VMvobzY"
sheet = client.open_by_key(SHEET_ID).sheet1

# AI lead scorer
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

def add_lead(name, email, company, message):
    print("\nAI scoring your lead...")
    ai_response = score_lead(name, email, company, message)
    
    lines = ai_response.strip().split('\n')
    score = lines[0].replace('Score: ', '')
    status = lines[1].replace('Status: ', '')
    
    sheet.append_row([name, email, company, message, score, status])
    print(f"\nLead added to CRM!")
    print(f"AI Score: {score}")
    print(f"Status: {status}")
    print(f"Reason: {lines[2].replace('Reason: ', '')}")

# Main
print("CRM Lead System\n")
print("Enter lead details:\n")
name = input("Name: ")
email = input("Email: ")
company = input("Company: ")
message = input("Message/Requirement: ")

add_lead(name, email, company, message)