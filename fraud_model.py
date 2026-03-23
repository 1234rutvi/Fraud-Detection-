from sklearn.ensemble import IsolationForest

def detect_fraud(df):

    # ✅ 1. Check if dataframe exists
    if df is None or df.empty:
        raise ValueError("Uploaded file has no data.")

    # ✅ 2. Clean column names
    df.columns = df.columns.str.strip()

    # ✅ 3. Check column exists
    if "Amount" not in df.columns:
        raise ValueError(f"'Amount' column not found. Available columns: {df.columns.tolist()}")

    # ✅ 4. Remove null values
    df = df.dropna(subset=["Amount"])

    # ✅ 5. Ensure numeric values
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Amount"])

    # ✅ 6. Check again after cleaning
    if df.shape[0] == 0:
        raise ValueError("No valid transaction amounts found.")

    # ✅ 7. Apply model
    model = IsolationForest(contamination=0.02, random_state=42)

    df["Anomaly"] = model.fit_predict(df[["Amount"]])

    df["ML_Flag"] = df["Anomaly"].apply(
        lambda x: "Fraud" if x == -1 else "Normal"
    )

    return df
