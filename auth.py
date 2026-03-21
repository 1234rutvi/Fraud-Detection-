import streamlit as st
import sqlite3

# DB setup
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
# 🎨 SPLIT SCREEN STYLE
# -----------------------------
def split_style():
    st.markdown("""
    <style>
    .container {
        display: flex;
        height: 90vh;
    }
    .left {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #0e1117;
    }
    .right {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #1c1f26;
    }
    .form-box {
        background-color: #262730;
        padding: 30px;
        border-radius: 15px;
        width: 300px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------
# 🔐 LOGIN UI
# -----------------------------
def login():
    split_style()

    col1, col2 = st.columns(2)

    # LEFT SIDE → LOGO
    with col1:
        st.image("logo.png", use_column_width=True)

    # RIGHT SIDE → FORM
    with col2:
        st.markdown('<div class="form-box">', unsafe_allow_html=True)
        st.subheader("🔐 Login")

        user = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, password))
            if cursor.fetchone():
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
            else:
                st.error("Invalid credentials")

        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 📝 SIGNUP UI
# -----------------------------
def signup():
    split_style()

    col1, col2 = st.columns(2)

    with col1:
        st.image("logo.png", use_column_width=True)

    with col2:
        st.markdown('<div class="form-box">', unsafe_allow_html=True)
        st.subheader("📝 Sign Up")

        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Sign Up"):
            cursor.execute("SELECT * FROM users WHERE username=?", (new_user,))
            if cursor.fetchone():
                st.error("User already exists!")
            else:
                cursor.execute("INSERT INTO users VALUES (?, ?)", (new_user, new_pass))
                conn.commit()
                st.success("Account created! Please login.")

        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 🔁 SWITCH PAGE
# -----------------------------
def auth_page():
    option = st.radio("", ["Login", "Sign Up"], horizontal=True)

    if option == "Login":
        login()
    else:
        signup()

# -----------------------------
# 🔐 CHECK AUTH
# -----------------------------
def check_auth():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        auth_page()
        st.stop()
