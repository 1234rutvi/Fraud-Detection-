import streamlit as st
import sqlite3
import os

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
# 🎨 BACKGROUND + GLASS UI
# -----------------------------
def apply_style():
    st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }

    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }

    .glass {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# 🖼️ LOAD LOGO
# -----------------------------
def load_logo():
    logo_path = os.path.join(os.getcwd(), "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=350)
    else:
        st.warning("Logo not found")

# -----------------------------
# 🔐 LOGIN
# -----------------------------
def login():
    apply_style()

    col1, col2 = st.columns(2)

    with col1:
        load_logo()
        st.markdown(
            "<h2 style='text-align:center;color:white;'>Fraud Detection System</h2>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("🔐 Login")

        user = st.text_input("Username", key="login_user").strip()
        password = st.text_input("Password", type="password", key="login_pass").strip()

        if st.button("Login", key="login_btn"):
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

        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 📝 SIGNUP
# -----------------------------
def signup():
    apply_style()

    col1, col2 = st.columns(2)

    with col1:
        load_logo()
        st.markdown(
            "<h2 style='text-align:center;color:white;'>Create Your Account</h2>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("📝 Sign Up")

        new_user = st.text_input("Create Username", key="signup_user").strip()
        new_pass = st.text_input("Create Password", type="password", key="signup_pass").strip()

        if st.button("Sign Up", key="signup_btn"):
            if not new_user or not new_pass:
                st.warning("Fill all fields")
                return

            cursor.execute("SELECT * FROM users WHERE username=?", (new_user,))
            if cursor.fetchone():
                st.error("User already exists!")
            else:
                cursor.execute("INSERT INTO users VALUES (?, ?)", (new_user, new_pass))
                conn.commit()

                st.success("Account created successfully! Redirecting to login...")

                # 🔁 AUTO SWITCH TO LOGIN
                st.session_state["show_login"] = True
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 🔁 PAGE CONTROL
# -----------------------------
def auth_page():
    if "show_login" not in st.session_state:
        st.session_state["show_login"] = True

    option = st.radio(
        "",
        ["Login", "Sign Up"],
        horizontal=True,
        index=0 if st.session_state["show_login"] else 1
    )

    if option == "Login":
        st.session_state["show_login"] = True
        login()
    else:
        st.session_state["show_login"] = False
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
