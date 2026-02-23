import streamlit as st
import json
import os
from pathlib import Path
from datetime import date

# 1. SET PAGE CONFIG (Must be the very first Streamlit command)
st.set_page_config(
    page_title="Helpdesk & Assistant",
    page_icon="🛠️",
    layout="wide"
)

# --- CONSTANTS & HELPERS ---
USERS_FILE = "users.json"
GOALS_FILE = Path("goals.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def load_goals():
    if GOALS_FILE.exists():
        with open(GOALS_FILE, "r") as f:
            return json.load(f)
    return []

def save_goals(goals):
    with open(GOALS_FILE, "w") as f:
        json.dump(goals, f, indent=2)

# Ensure goals are in session state for consistency across pages
if "goals" not in st.session_state:
    st.session_state.goals = load_goals()

# --- PAGE DEFINITIONS ---

def auth_page():
    st.title("🔐 Sign In / Sign Up")
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
                    st.rerun()
                else:
                    st.error("Invalid login")
            else:
                if username in users:
                    st.error("User already exists")
                else:
                    users[username] = password
                    save_users(users)
                    st.success("Account created. Please Sign In.")

def home_page():
    st.title(f"👋 Welcome back, {st.session_state.user}!")
    
    # Use session state goals so it matches the tracker exactly
    goals = st.session_state.goals
    
    if not goals:
        st.info("You haven't set any goals yet. Head over to the **Goal Tracker** to start!")
        return

    # --- Quick Stats Row ---
    total_goals = len(goals)
    completed_goals = sum(1 for g in goals if g.get("status") == "Completed")
    total_points = sum(g.get("points", 0) for g in goals if g.get("points_awarded"))

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Goals", total_goals)
    col2.metric("Completed", completed_goals)
    col3.metric("Points Earned", f"⭐ {total_points}")

    st.divider()

    # --- Goals Preview Table ---
    st.subheader("📋 Current Goals Preview")
    
    preview_data = []
    for g in goals:
        preview_data.append({
            "Goal": g.get("title", "Untitled"),
            "Status": g.get("status", "Not Started"),
            "Target": f"${g.get('money_target', 0)}",
            "Target Date": g.get("target_date", "Not set")
        })
    
    st.table(preview_data)

def feature1_page():
    st.title("📚 Support Schemes Overview")
    folder = "schemes"

    if not os.path.exists(folder):
        os.makedirs(folder)
        st.info(f"Folder '{folder}' created. Add text files there.")
        return

    txt_files = sorted([f for f in os.listdir(folder) if f.endswith(".txt")])

    if not txt_files:
        st.warning("No scheme files found.")
    else:
        for file_name in txt_files:
            scheme_name = os.path.splitext(file_name)[0].replace("_", " ").title()
            try:
                with open(os.path.join(folder, file_name), "r", encoding="utf-8") as f:
                    content = f.read()
                    with st.expander(scheme_name):
                        st.markdown(content, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error reading {file_name}: {e}")

def feature2_page():
    st.title("Goal Tracker")
    st.subheader("🎯 Your Goals")

    STATUS_META = {
        "Not Started": "⏳",
        "In Progress": "🔄",
        "Blocked": "⛔",
        "Completed": "✅",
    }

    # ⭐ Total points calculation
    total_points = sum(
        goal.get("points", 0)
        for goal in st.session_state.goals
        if goal.get("points_awarded", False)
    )
    st.sidebar.metric("⭐ Total Points", total_points)

    # Display goals
    if st.session_state.goals:
        cols = st.columns(2)
        for i, goal in enumerate(st.session_state.goals):
            with cols[i % 2]:
                with st.container(border=True):
                    st.subheader(f"{STATUS_META.get(goal['status'], '❓')} {goal['title']}")
                    
                    # Display Description if it exists
                    if goal.get("description"):
                        st.caption(goal["description"])

                    # Editable status
                    status_options = list(STATUS_META.keys())
                    current_status_index = status_options.index(goal["status"]) if goal["status"] in status_options else 0
                    
                    new_status = st.selectbox("Status", status_options, index=current_status_index, key=f"status_{i}")

                    if new_status == "Completed" and not goal.get("points_awarded", False):
                        goal["points_awarded"] = True
                        st.balloons()
                        st.success(f"+{goal['points']} points earned!")

                    goal["status"] = new_status

                    # Only show money target if it's a financial goal
                    if goal.get("type") == "Financial":
                        st.write(f"💰 Savings Target: **${goal.get('money_target', 0)}**")
                    
                    st.write(f"⭐ Points: **{goal.get('points', 0)}**")
                    st.write(f"📅 Target Date: **{goal.get('target_date', 'N/A')}**")
                    st.write("🏅 Awarded: " + ("✅ Yes" if goal.get("points_awarded") else "❌ No"))

        save_goals(st.session_state.goals)
    else:
        st.info("No goals added yet.")

    st.divider()

    # ➕ Add new goal form
    st.subheader("➕ Add a New Goal")
    with st.form("new_goal_form"):
        goal_title = st.text_input("Goal name")
        goal_description = st.text_area("Description", help="Describe what you want to achieve")
        
        # TOGGLE LOGIC: Select Type
        goal_type = st.radio("Goal Type", ["General", "Financial"], horizontal=True)
        
        # This input will be processed based on the goal_type choice above
        money_target = st.number_input("Amount to save ($)", min_value=0.0, step=10.0)
        
        col_a, col_b = st.columns(2)
        points = col_a.number_input("Points for completion", min_value=0, step=1)
        target_date = col_b.date_input("Target date", min_value=date.today())
        
        if st.form_submit_button("Add Goal"):
            if goal_title.strip():
                new_goal = {
                    "title": goal_title.strip(),
                    "description": goal_description.strip(),
                    "type": goal_type,
                    "status": "Not Started",
                    "money_target": money_target if goal_type == "Financial" else 0,
                    "points": points,
                    "points_awarded": False,
                    "target_date": target_date.isoformat()
                }
                st.session_state.goals.append(new_goal)
                save_goals(st.session_state.goals)
                st.success("Goal added!")
                st.rerun()
            else:
                st.warning("Goal name cannot be empty.")


# --- MAIN APP ROUTING ---

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    auth_page()
else:
    # Navigation Sidebar
    st.sidebar.title(f"User: {st.session_state.user}")
    page = st.sidebar.radio("Navigation", ["Home", "Support Schemes", "Goal Tracker", "Assistant Chat"])
    
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.goals = [] # Clear goals on logout
        st.rerun()

    # Load Pages
    if page == "Home":
        home_page()
    elif page == "Support Schemes":
        feature1_page()
    elif page == "Goal Tracker":
        feature2_page()
        

