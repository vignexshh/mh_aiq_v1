import streamlit as st
import sqlite3
import pandas as pd

# Function to fetch data based on the dynamic query
def fetch_data(query, db_file='neet_candidates.db'):
    with sqlite3.connect(db_file) as conn:
        df = pd.read_sql_query(query, conn)
    return df

def main():
    st.title("Neet UG-2024 AP Results")

    # Set up user inputs in the sidebar
    st.sidebar.header("Filter Options")
    
    # Input fields
    rank = st.sidebar.text_input("Rank")
    allotted_quota = st.sidebar.selectbox("Allotted Quota", [
        "Select All", "Open Seat Quota", "All India", "Delhi University Quota",
        "Deemed/Paid Seats Quota", "IP University Quota", "Foreign Country Quota",
        "Aligarh Muslim University (AMU) Quota", "Internal -Puducherry UT Domicile",
        "Employees State Insurance Scheme(ESI)", "Delhi NCR Children/Widows of Personnel of the Armed Forces (CW) Quota",
        "Non-Resident Indian", "Muslim OBC Quota", "Muslim Quota", "Muslim Women Quota",
        "Muslim Minority Quota", "B.Sc Nursing Delhi NCR", "Jamia Internal Quota",
        "Jain Minority Quota", "B.Sc Nursing Delhi NCR CW Quota", "Muslim ST Quota",
        "Employees State Insurance Scheme Nursing Quota (ESIIP Quota Nursing)",
        "Non-Resident Indian(AMU)Quota", "B.Sc Nursing All India"
    ])
    course = st.sidebar.selectbox("Course", ["Select All", "MBBS", "BDS", "B.Sc. Nursing"])
    allotted_category = st.sidebar.selectbox("Allotted Category", [
        "Select All", "OBC", "OBC PwD", "General Pwd", "Open", "Open PwD",
        "SC", "SC PwD", "ST", "ST PwD", "EWS PwD", "EWS"
    ])
    candidate_category = st.sidebar.selectbox("Candidate Category", [
        "Select All", "OBC", "OBC PwD", "General Pwd", "Open", "Open PwD",
        "SC", "SC PwD", "ST", "ST PwD", "EWS PwD", "EWS"
    ])

    # Generate the SQL query dynamically
    query = "SELECT * FROM neet_candidates WHERE 1=1"
    
    if rank:
        query += f" AND Rank = {rank}"
    if allotted_quota != "Select All":
        query += f" AND `Allotted quota` = '{allotted_quota}'"
    if course != "Select All":
        query += f" AND Course = '{course}'"
    if allotted_category != "Select All":
        query += f" AND `Allotted category` = '{allotted_category}'"
    if candidate_category != "Select All":
        query += f" AND `Candidate category` = '{candidate_category}'"

    # Fetch and display the data
    df = fetch_data(query)
    
    # Drop the candidate_name column if it exists
    if 'candidate_name' in df.columns:
        df = df.drop(columns=['candidate_name'])
    
    # Adjust the index to start from 1
    df.index = df.index + 1
    
    st.write(df)

if __name__ == "__main__":
    main()
