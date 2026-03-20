import streamlit as st
import pandas as pd

from parser import extract_pdf_data_advanced
from fraud_model import detect_fraud
from chatbot import chatbot
from database import save_to_db
from utils import categorize_ai

st.set_page_config(page_title="Fraud Detection System", layout="wide")

st.title("💳 Bank Statement Fraud Detection System")

file = st.file_uploader("Upload Bank Statement (CSV or PDF)", type=["csv", "pdf"])

if file:
    # Load file
    if file.type == "text/csv":
        df = pd.read_csv(file)
    else:
        df = extract_pdf_data_advanced(file)

    st.subheader("📄 Raw Data")
    st.dataframe(df)

    # Clean data
    df = df.dropna()
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna()

    # Categorization
    df["Category"] = df["Description"].astype(str).apply(categorize_ai)

    # Fraud detection
    df = detect_fraud(df)

    # Save to database
    save_to_db(df)

    st.subheader("🚨 Fraud Detection Results")
    st.dataframe(df)

    # Dashboard
    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", len(df))
    col2.metric("Fraud Detected", len(df[df["ML_Flag"] == "Fraud"]))
    col3.metric("Total Amount", f"₹ {df['Amount'].sum():,.2f}")

    st.bar_chart(df["Category"].value_counts())

    # Chatbot
    st.subheader("🤖 Ask Your Data")
    query = st.text_input("Ask something (e.g. total, fraud, food)")

    if query:
        response = chatbot(query, df)
        st.write(response)

else:
    st.info("Please upload a file to start.")
