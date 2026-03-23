import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_fraud(df):

    if df is None or df.empty:
        raise ValueError("No data available")

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Amount"])

    # -----------------------------
    # 🤖 ML MODEL
    # -----------------------------
    model = IsolationForest(contamination=0.02, random_state=42)
    df["Anomaly"] = model.fit_predict(df[["Amount"]])

    df["ML_Flag"] = df["Anomaly"].apply(
        lambda x: "Fraud" if x == -1 else "Normal"
    )

    # -----------------------------
    # 🚨 RULE-BASED DETECTION
    # -----------------------------
    df["Rule_Flag"] = "Normal"

    # Rule 1: High amount transaction
    df.loc[df["Amount"] > 20000, "Rule_Flag"] = "Fraud"

    # Rule 2: Negative large debit
    df.loc[df["Amount"] < -15000, "Rule_Flag"] = "Fraud"

    # Rule 3: Suspicious keywords
    suspicious_keywords = ["intl", "foreign", "unknown", "crypto", "bitcoin"]

    df["Description"] = df["Description"].astype(str).str.lower()

    df.loc[
        df["Description"].str.contains("|".join(suspicious_keywords), na=False),
        "Rule_Flag"
    ] = "Fraud"

    # -----------------------------
    # 🔥 FINAL DECISION
    # -----------------------------
    df["Final_Flag"] = df.apply(
        lambda row: "Fraud" if (row["ML_Flag"] == "Fraud" or row["Rule_Flag"] == "Fraud")
        else "Normal",
        axis=1
    )

    return df
