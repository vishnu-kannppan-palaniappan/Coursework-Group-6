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
if "page" not in st.session_state:
    st.session_state.page = "auth"

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

    # home buttons to go to features
    col1, col2, col3 = st.columns(3)
    if col1.button("Feature 1"):
        st.session_state.page = "feature1"
    if col2.button("Feature 2"):
        st.session_state.page = "feature2"
    if col3.button("Feature 3"):
        st.session_state.page = "feature3"

    if st.button("Log out"):
        st.session_state.user = None
        st.session_state.page = "auth"

def feature1_page():
    st.title("Feature 1")
    st.write("This is feature 1")
    if st.button("Back to Home"):
        st.session_state.page = "home"

def feature2_page():
    st.title("Feature 2")
    st.write("This is feature 2")
    if st.button("Back to Home"):
        st.session_state.page = "home"

def feature3_page():
    st.title("Feature 3")
    st.write("This is feature 3")
    if st.button("Back to Home"):
        st.session_state.page = "home"

if st.session_state.user:
    page = st.sidebar.selectbox("Navigation", ["Home", "Feature 1", "Feature 2", "Feature 3"])
    if page == "Home":
        st.session_state.page = "home"
    elif page == "Feature 1":
        st.session_state.page = "feature1"
    elif page == "Feature 2":
        st.session_state.page = "feature2"
    elif page == "Feature 3":
        st.session_state.page = "feature3"

if st.session_state.user is None:
    auth_page()
else:
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "feature1":
        feature1_page()
    elif st.session_state.page == "feature2":
        feature2_page()
    elif st.session_state.page == "feature3":
        feature3_page()
