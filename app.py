import streamlit as st
import pandas as pd
import plotly.express as px
import tempfile

from auth import check_auth
from parser import extract_pdf_data_advanced
from fraud_model import detect_fraud
from chatbot import chatbot
from database import save_to_db
from utils import categorize_ai
from alerts import send_email_alert

# -----------------------------
# 🔐 AUTH (MUST BE FIRST)
# -----------------------------
check_auth()

# Sidebar user info + logout
st.sidebar.success(f"Logged in as {st.session_state['user']}")

if st.sidebar.button("🚪 Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

# -----------------------------
# 🎨 PAGE CONFIG + STYLE
# -----------------------------
st.set_page_config(page_title="Fraud Detection System", layout="wide")

st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
div[data-testid="stMetric"] {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🏷️ HEADER
# -----------------------------
st.markdown("""
# 💳 Fraud Detection System
### Upload your bank statement (CSV/PDF) to detect suspicious transactions and gain insights.
""")

st.markdown("---")

# -----------------------------
# 📂 FILE UPLOAD
# -----------------------------
file = st.file_uploader("📂 Upload Bank Statement (CSV or PDF)", type=["csv", "pdf"])

if file:

    # -----------------------------
    # 📥 LOAD FILE (FIXED FOR RENDER)
    # -----------------------------
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        df = extract_pdf_data_advanced(tmp_path)

    st.subheader("📄 Raw Data")
    st.dataframe(df)

    # -----------------------------
    # 🧹 CLEAN DATA
    # -----------------------------
    df = df.dropna()
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna()

    # -----------------------------
    # 🧠 CATEGORY DETECTION
    # -----------------------------
    df["Category"] = df["Description"].astype(str).apply(categorize_ai)

    # -----------------------------
    # 🤖 FRAUD DETECTION
    # -----------------------------
    with st.spinner("🔍 Analyzing transactions..."):
        df = detect_fraud(df)

    # -----------------------------
    # 💾 SAVE TO DATABASE
    # -----------------------------
    save_to_db(df)

    # -----------------------------
    # 📊 KPI METRICS
    # -----------------------------
    fraud_df = df[df["ML_Flag"] == "Fraud"]

    col1, col2, col3 = st.columns(3)

    col1.metric("💳 Total Transactions", len(df))
    col2.metric("🚨 Fraud Detected", len(fraud_df))
    col3.metric("💰 Total Amount", f"₹ {df['Amount'].sum():,.2f}")

    # -----------------------------
    # 📈 CHARTS
    # -----------------------------
    st.markdown("---")
    st.subheader("📊 Financial Insights")

    fig1 = px.pie(df, names="Category", values="Amount", title="Spending by Category")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(df, y="Amount", title="Transaction Trend")
    st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # 🚨 FRAUD SECTION + EMAIL
    # -----------------------------
    st.markdown("---")
    st.subheader("🚨 Suspicious Transactions")

    if not fraud_df.empty:
        st.error(f"{len(fraud_df)} suspicious transactions detected!")
        st.dataframe(fraud_df)

        
    # -----------------------------
    # 🤖 CHATBOT
    # -----------------------------
    st.markdown("---")
    st.subheader("🤖 Ask Your Data")

    query = st.text_input("Ask something like 'total', 'fraud', 'food'")

    if query:
        response = chatbot(query, df)
        st.write(response)

    # -----------------------------
    # 📥 DOWNLOAD
    # -----------------------------
    st.markdown("---")

    st.download_button(
        label="📥 Download Full Report",
        data=df.to_csv(index=False),
        file_name="fraud_report.csv",
        mime="text/csv"
    )

else:
    st.warning("📂 Please upload a bank statement to begin analysis.")
