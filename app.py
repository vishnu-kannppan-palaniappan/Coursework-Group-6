import streamlit as st
import json
import os

USERS_FILE = "users.json"

st.set_page_config(page_title="app support?", layout="wide")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "auth"

def auth_page():
    st.title("Sign In / Sign Up")
    mode = st.radio("Mode", ["Sign In", "Sign Up"])

    with st.form("auth_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button(mode)

        if submit:
            users = load_users()
            if mode == "Sign In":
                if username in users and users[username] == password:
                    st.session_state.user = username
                    st.session_state.page = "home"
                else:
                    st.error("Invalid login")
            else:
                if username in users:
                    st.error("User already exists")
                else:
                    users[username] = password
                    save_users(users)
                    st.success("Account created. Sign in now.")

def home_page():
    st.title("Home")
    st.write(f"Welcome, {st.session_state.user}")

def feature1_page():
    # Big page-wide title
    st.title("Support Schemes Overview")

    # 3 columns for 3 schemes
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Silver Support Scheme")
        st.markdown("""
### Objective The *Silver Support Scheme (SSS)* aims to provide financial support to *elderly Singapore citizens* who have lower lifetime incomes and limited family support. --- ### Basic Eligibility Criteria An individual must: - Be a *Singapore Citizen* - Have *attained 65 years of age* - Satisfy all other prescribed eligibility criteria --- ### Clarifications for Attaining 65 Years of Age - An individual attains *65 years of age on the 65th anniversary* of their birth date - If born on *29 February, the 65th anniversary is deemed to occur on **1 March* - If the *day of birth cannot be ascertained, it is deemed to be the **1st day of that month* - If the *month of birth cannot be ascertained, it is deemed to be **January* --- ### Monetary Eligibility Requirements - *CPF Contributions* by age 55 must not exceed *SGD 140,000* - *Self-employed / platform workers*: - Average annual net trade income (ages 45–54) must not exceed *SGD 27,600* - Must live in a *1- to 5-room HDB flat* - Neither the individual nor their spouse should own: - A *5-room or larger HDB flat* - *Any private property* - *Multiple properties* - *Monthly household income per person* must not exceed *SGD 2,300* --- ### Benefits (Annual Payout) #### Living in 1- and 2-room HDB flats - Income ≤ $1,500 → *$1,080* - Income > $1,500 and ≤ $2,300 → *$540* #### Living in 3-room HDB flats - Income ≤ $1,500 → *$860* - Income > $1,500 and ≤ $2,300 → *$430* #### Living in 4-room HDB flats - Income ≤ $1,500 → *$650* - Income > $1,500 and ≤ $2,300 → *$325* #### Living in 5-room HDB flats* (not owned by the senior) - Income ≤ $1,500 → *$430* - Income > $1,500 and ≤ $2,300 → *$215* --- \* Seniors must *not own* the 5-room flat.
""")

    with col2:
        st.header("Gold Support Scheme")
        st.markdown("""
- Objective: Aid middle-income families
- Eligibility: Singapore Citizen, 50–64 years
- Benefits: Monthly subsidies for healthcare and housing
""")

    with col3:
        st.header("Platinum Support Scheme")
        st.markdown("""
- Objective: Assist low-income families
- Eligibility: Singapore Citizen, any adult
- Benefits: Cash grants, educational support for children
""")


def feature2_page():
    st.title("Feature 2")
    st.write("This is feature 2")

def helpdesk_page():
    st.title("Helpdesk")
    st.write("This is the helpdesk")

if st.session_state.user:
    with st.sidebar:
        st.title("Navigation")

        if st.button("Home"):
            st.session_state.page = "home"
        if st.button("Feature 1"):
            st.session_state.page = "feature1"
        if st.button("Feature 2"):
            st.session_state.page = "feature2"
        if st.button("Helpdesk"):
            st.session_state.page = "helpdesk"

        st.divider()
        if st.button("Log out"):
            st.session_state.user = None
            st.session_state.page = "auth"

if st.session_state.user is None:
    auth_page()
else:
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "feature1":
        feature1_page()
    elif st.session_state.page == "feature2":
        feature2_page()
    elif st.session_state.page == "helpdesk":
        helpdesk_page()
