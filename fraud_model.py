from sklearn.ensemble import IsolationForest

def detect_fraud(df):
    model = IsolationForest(contamination=0.02, random_state=42)

    df["Anomaly"] = model.fit_predict(df[["Amount"]])

    df["ML_Flag"] = df["Anomaly"].apply(
        lambda x: "Fraud" if x == -1 else "Normal"
    )

    return df
