import streamlit as st
import sqlite3
import os
import base64

# -----------------------------
# 💾 DATABASE
# -----------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
""")
conn.commit()

# -----------------------------
# 🌌 BACKGROUND (SAFE)
# -----------------------------
def set_background():
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}

        /* FIX INPUT VISIBILITY */
        label, .stTextInput label {{
            color: white !important;
        }}

        /* BUTTON FULL WIDTH */
        .stButton > button {{
            width: 100%;
            border-radius: 8px;
        }}
        </style>
        """, unsafe_allow_html=True)

# -----------------------------
# 🔐 LOGIN
# -----------------------------
def login():
    set_background()

    st.markdown("## 🔐 Login")

    user = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        user = user.strip()
        password = password.strip()

        if not user or not password:
            st.warning("Enter username & password")
        else:
            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (user, password)
            )

            if cursor.fetchone():
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("Invalid credentials")

    if st.button("Create New Account"):
        st.session_state["page"] = "signup"
        st.rerun()

# -----------------------------
# 📝 SIGNUP
# -----------------------------
def signup():
    set_background()

    st.markdown("## 📝 Sign Up")

    new_user = st.text_input("Create Username", key="signup_user")
    new_pass = st.text_input("Create Password", type="password", key="signup_pass")

    if st.button("Sign Up"):
        new_user = new_user.strip()
        new_pass = new_pass.strip()

        if not new_user or not new_pass:
            st.warning("Fill all fields")
        else:
            cursor.execute("SELECT * FROM users WHERE username=?", (new_user,))
            if cursor.fetchone():
                st.error("User already exists!")
            else:
                cursor.execute("INSERT INTO users VALUES (?, ?)", (new_user, new_pass))
                conn.commit()

                st.success("Account created! Redirecting...")
                st.session_state["page"] = "login"
                st.rerun()

    if st.button("Already have an account? Login"):
        st.session_state["page"] = "login"
        st.rerun()

# -----------------------------
# 🔁 PAGE CONTROL
# -----------------------------
def auth_page():
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if st.session_state["page"] == "login":
        login()
    else:
        signup()

# -----------------------------
# 🔐 AUTH CHECK
# -----------------------------
def check_auth():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        auth_page()
        st.stop()
