import streamlit as st
import sqlite3
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
import bcrypt

# Initialize Firebase Admin SDK only if it's not already initialized
if not firebase_admin._apps:
    try:
        # Load Firebase credentials
        cred = credentials.Certificate('medi-rakesh-503bc-firebase-adminsdk-pfk5i-69f267ec31.json')
        # Initialize Firebase app with credentials and database URL
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://medi-rakesh-503bc-default-rtdb.firebaseio.com/'
        })
        print("Firebase Initialized")
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")

# Set page configuration
st.set_page_config(
    page_title="Neet UG-2024 Results",
    page_icon="favicon.ico",  # Path to your favicon file
    layout="wide"
)

def fetch_data(query, db_file='neet_candidates.db'):
    with sqlite3.connect(db_file) as conn:
        df = pd.read_sql_query(query, conn)
    return df

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8'), salt.decode('utf-8')

def verify_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

def authenticate_user(username, password):
    try:
        # Reference to the user in Firebase Realtime Database
        user_ref = db.reference("user_details").child(username)
        user_data = user_ref.get()

        if user_data:
            # Verify password
            stored_hash = user_data.get("hashed_password")
            if stored_hash and verify_password(stored_hash, password):
                # Check if the user is in RequestedUsers
                requested_user_ref = db.reference("requested_users").child(username)
                requested_user_data = requested_user_ref.get()

                if requested_user_data:
                    return "User not yet accepted"

                # Check if the user is in AcceptedUsers
                accepted_user_ref = db.reference("accepted_users").child(username)
                accepted_user_data = accepted_user_ref.get()

                if accepted_user_data:
                    return "Authenticated"
                else:
                    return "Invalid username or password"
            else:
                return "Invalid username or password"
        else:
            return "Invalid username or password"
    except Exception as e:
        return f"Authentication error: {str(e)}"

def main():
    st.markdown("""
        <title>MedicalHunt Neet UG-2024 All India Quota Results | Round-01</title>
        <meta name="description" content="View NEET UG-2024 All India Quota Results for Round-01. Filter results based on rank, quota, course, and category.">
        <meta property="og:title" content="Neet UG-2024 All India Quota Results | Round-01">
        <meta property="og:description" content="View NEET UG-2024 All India Quota Results for Round-01. Filter results based on rank, quota, course, and category.">
        <meta property="og:image" content="https://example.com/path/to/your/open-graph-image.jpg">
        <meta property="og:url" content="https://example.com">
        <link rel="icon" href="favicon.ico">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
            }
            .author-section {
                display: flex;
                align-items: center;
            }
            .author-icon {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                margin-right: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Neet UG-2024 All India Quota Results | Round-01")

    # Initialize session state variables if not already present
    if "auth_status" not in st.session_state:
        st.session_state.auth_status = None
    if "username" not in st.session_state:
        st.session_state.username = None

    if st.session_state.auth_status == "Authenticated":
        # Main app content
        st.markdown("""
            <div class="author-section">
                <div>
                    <strong>Data Sorted By :</strong> MedicalHunt
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            
        """)

        # Create columns
        col1, col2 = st.columns(2)

        with col1:
            st.header("Filter Options")
            rank_input = st.text_input("Rank", key="rank_input")
            
            # Ensure rank_input is a valid integer
            if rank_input and not rank_input.isdigit():
                st.error("Rank must be a numerical value.")
                rank = None
            else:
                rank = rank_input

            allotted_quota = st.selectbox("Allotted Quota", [
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
            course = st.selectbox("Course", ["Select All", "MBBS", "BDS", "B.Sc. Nursing"])
            allotted_category = st.selectbox("Allotted Category", [
                "Select All", "OBC", "OBC PwD", "General Pwd", "Open", "Open PwD",
                "SC", "SC PwD", "ST", "ST PwD", "EWS PwD", "EWS"
            ])
            candidate_category = st.selectbox("Candidate Category", [
                "Select All", "OBC", "OBC PwD", "General Pwd", "Open", "Open PwD",
                "SC", "SC PwD", "ST", "ST PwD", "EWS PwD", "EWS"
            ])

        # Filter the data based on the user inputs
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

        df = fetch_data(query)
        
        # Drop the candidate_name column if it exists
        if 'candidate_name' in df.columns:
            df = df.drop(columns=['candidate_name'])
        
        # Adjust the index to start from 1
        df.index = df.index + 1
        
        with col2:
            st.write(df)
    else:
        # Display the login form if not authenticated
        st.header("Login")
        username_input = st.text_input("Username", key="username_input")
        password_input = st.text_input("Password", type="password", key="password_input")
        login_button = st.button("Login")
        logout_button = st.button("Logout")

        if logout_button:
            st.session_state.auth_status = None
            st.session_state.username = None
            st.success("Logged out successfully")
            st.rerun()

        if login_button:
            auth_status = authenticate_user(username_input, password_input)
            if auth_status == "Authenticated":
                st.session_state.auth_status = "Authenticated"
                st.session_state.username = username_input
                st.success("Login successful")
                st.rerun()
            else:
                st.error(auth_status)

if __name__ == "__main__":
    main()
