import sqlite3

conn = sqlite3.connect("fraud_app.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    date TEXT,
    description TEXT,
    amount REAL,
    category TEXT,
    fraud_flag TEXT
)
""")

conn.commit()

def save_to_db(df):
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO transactions VALUES (?, ?, ?, ?, ?)
        """, (
            row["Date"],
            row["Description"],
            row["Amount"],
            row["Category"],
            row["ML_Flag"]
        ))
    conn.commit()
