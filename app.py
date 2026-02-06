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
    st.title("Support Schemes Overview")

    # Folder containing all your txt files
    folder = "schemes"

    # Grab all txt files
    txt_files = sorted([f for f in os.listdir(folder) if f.endswith(".txt")])

    if not txt_files:
        st.error("No scheme files found in the folder!")
    else:
        for file_name in txt_files:
            # Remove file extension for expander title
            scheme_name = os.path.splitext(file_name)[0].replace("_", " ").title()
            file_path = os.path.join(folder, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Use st.expander to collapse/expand each scheme
                    with st.expander(scheme_name):
                        st.markdown(content, unsafe_allow_html=True)
            except FileNotFoundError:
                st.error(f"File missing: {file_name}")

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
