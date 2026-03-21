import streamlit as st
import sqlite3
import os
import base64

# -----------------------------
# 💾 DATABASE SETUP
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
# 🌌 BACKGROUND + RESPONSIVE UI
# -----------------------------
def set_background():
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
                url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        .glass-box {{
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            width: 90%;
            max-width: 360px;
            margin: auto;
            text-align: center;
        }}

        @media (max-width: 768px) {{
            .glass-box {{
                padding: 20px;
                width: 90%;
            }}
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ logo.png not found")

# -----------------------------
# 🎯 CENTER CONTAINER
# -----------------------------
def center_start():
    st.markdown("""
    <div style="
        display:flex;
        justify-content:center;
        align-items:center;
        min-height:100vh;
        padding:20px;
    ">
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)

def center_end():
    st.markdown("</div></div>", unsafe_allow_html=True)

# -----------------------------
# 🔐 LOGIN
# -----------------------------
def login():
    set_background()
    center_start()

    st.markdown("<h2 style='color:white;'>🔐 Login</h2>", unsafe_allow_html=True)
    st.caption("Secure Login • Fraud Detection System")

    user = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", use_container_width=True):
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

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Create New Account", use_container_width=True):
        st.session_state["page"] = "signup"
        st.rerun()

    center_end()

# -----------------------------
# 📝 SIGNUP
# -----------------------------
def signup():
    set_background()
    center_start()

    st.markdown("<h2 style='color:white;'>📝 Sign Up</h2>", unsafe_allow_html=True)
    st.caption("Create your account")

    new_user = st.text_input("Create Username", key="signup_user")
    new_pass = st.text_input("Create Password", type="password", key="signup_pass")

    if st.button("Sign Up", use_container_width=True):
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

                st.success("Account created! Redirecting to login...")
                st.session_state["page"] = "login"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Already have an account? Login", use_container_width=True):
        st.session_state["page"] = "login"
        st.rerun()

    center_end()

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
