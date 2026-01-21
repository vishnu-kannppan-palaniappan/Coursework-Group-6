import streamlit as st
import json
import os

USERS_FILE = "users.json"

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
if "login_success" not in st.session_state:
    st.session_state.login_success = False

def auth_page():
    st.title("Sign In / Sign Up")
    mode = st.radio("Mode", ["Sign In", "Sign Up"])

    with st.form(key="auth_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button(mode)

        if submit:
            users = load_users()
            if mode == "Sign In":
                if username in users and users[username] == password:
                    st.session_state.user = username
                    st.session_state.login_success = True
                else:
                    st.error("Invalid login")
            else:
                if username in users:
                    st.error("User already exists")
                else:
                    users[username] = password
                    save_users(users)
                    st.success("Account created. Sign in now.")

    if st.session_state.login_success:
        st.session_state.login_success = False
        st.experimental_rerun()

def home_page():
    st.title("Home")
    st.write(f"Welcome, {st.session_state.user}")

    if st.button("Log out"):
        st.session_state.user = None
        st.experimental_rerun()

if st.session_state.user is None:
    auth_page()
else:
    home_page()

