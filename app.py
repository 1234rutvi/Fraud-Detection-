import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load trained model
model = joblib.load("fraud_model.pkl")

st.title("💳 AI Fraud Detection System")

st.write("Enter transaction details to check if it is fraudulent.")

# Input fields
time = st.number_input("Transaction Time")
amount = st.number_input("Transaction Amount")

if st.button("Check Transaction"):

    input_data = np.array([[time, amount]])

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.error("⚠ Fraudulent Transaction Detected")
    else:
        st.success("✅ Transaction is Safe")

st.subheader("Upload Transactions CSV")

uploaded_file = st.file_uploader("Upload CSV")

if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    predictions = model.predict(data)

    data["Fraud_Prediction"] = predictions

    st.write(data)

    fraud_count = sum(predictions)

    st.write("Fraud Transactions Detected:", fraud_count)
