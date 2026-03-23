import pdfplumber
import pandas as pd

def extract_pdf_data_advanced(file_path):

    all_rows = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                for row in table:
                    if row:
                        all_rows.append(row)

    if not all_rows:
        return pd.DataFrame()

    # Convert to DataFrame
    df = pd.DataFrame(all_rows)

    # First row as header
    df.columns = df.iloc[0]
    df = df[1:]

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # -----------------------------
    # 🧠 COLUMN STANDARDIZATION
    # -----------------------------
    col_map = {}

    for col in df.columns:
        col_lower = col.lower()

        if "date" in col_lower:
            col_map[col] = "Date"

        elif "desc" in col_lower or "narration" in col_lower:
            col_map[col] = "Description"

        elif "debit" in col_lower:
            col_map[col] = "Debit"

        elif "credit" in col_lower:
            col_map[col] = "Credit"

        elif "amount" in col_lower:
            col_map[col] = "Amount"

    df = df.rename(columns=col_map)

    # -----------------------------
    # 💰 CREATE FINAL AMOUNT COLUMN
    # -----------------------------
    if "Amount" not in df.columns:

        if "Debit" in df.columns:
            df["Debit"] = pd.to_numeric(df["Debit"], errors="coerce").fillna(0)
        else:
            df["Debit"] = 0

        if "Credit" in df.columns:
            df["Credit"] = pd.to_numeric(df["Credit"], errors="coerce").fillna(0)
        else:
            df["Credit"] = 0

        # Debit = negative, Credit = positive
        df["Amount"] = df["Credit"] - df["Debit"]

    # -----------------------------
    # 🧹 CLEAN DATA
    # -----------------------------
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df = df.dropna(subset=["Amount"])

    # Keep only important columns
    keep_cols = ["Date", "Description", "Amount"]
    df = df[[col for col in keep_cols if col in df.columns]]

    return df.reset_index(drop=True)
