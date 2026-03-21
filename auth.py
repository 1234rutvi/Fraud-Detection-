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
# SIGNUP FUNCTION
# -----------------------------
def signup():
    st.title("📝 Sign Up")

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

# -----------------------------
# LOGIN FUNCTION
# -----------------------------
def login():
    st.title("🔐 Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, password))
        if cursor.fetchone():
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
        else:
            st.error("Invalid credentials")

# -----------------------------
# MAIN AUTH PAGE
# -----------------------------
def auth_page():
    choice = st.sidebar.radio("Select Option", ["Login", "Sign Up"])

    if choice == "Login":
        login()
    else:
        signup()

# -----------------------------
# CHECK AUTH
# -----------------------------
def check_auth():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        auth_page()
        st.stop()
