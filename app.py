import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px

# Load trained model
model = joblib.load("fraud_model.pkl")

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

st.title("💳 AI Fraud Detection System")

st.write("Machine Learning system to detect fraudulent transactions.")

# Sidebar inputs
st.sidebar.header("Transaction Details")

time = st.sidebar.number_input("Transaction Time", value=0)
amount = st.sidebar.number_input("Transaction Amount", value=0)

v1 = st.sidebar.number_input("V1", value=0.0)
v2 = st.sidebar.number_input("V2", value=0.0)
v3 = st.sidebar.number_input("V3", value=0.0)

if st.sidebar.button("Analyze Transaction"):

    input_data = np.array([[time, v1, v2, v3, amount]])

    prediction = model.predict(input_data)

    prob = model.predict_proba(input_data)[0][1] * 100

    col1, col2 = st.columns(2)

    with col1:

        if prediction[0] == 1:
            st.error("⚠ Fraudulent Transaction Detected")
        else:
            st.success("✅ Transaction is Legitimate")

    with col2:

        st.metric("Fraud Risk Score", f"{prob:.2f}%")

# Upload dataset
st.subheader("📂 Upload Transaction Dataset")

uploaded_file = st.file_uploader("Upload CSV file")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, encoding="latin1")
    st.write(data.head())

 

    predictions = model.predict(data)

    data["Fraud Prediction"] = predictions

    fraud_count = sum(predictions == 1)
    normal_count = sum(predictions == 0)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Fraud Transactions", fraud_count)

    with col2:
        st.metric("Normal Transactions", normal_count)

    st.subheader("Fraud Analytics")

    chart_data = pd.DataFrame({
        "Transaction Type": ["Fraud", "Normal"],
        "Count": [fraud_count, normal_count]
    })

    fig = px.pie(chart_data,
                 values="Count",
                 names="Transaction Type",
                 title="Fraud vs Normal Transactions")

    st.plotly_chart(fig)

    st.subheader("Dataset Preview")
    st.write(data.head())
