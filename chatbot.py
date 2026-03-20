def chatbot(query, df):
    query = query.lower()

    if "food" in query:
        total = df[df["Category"] == "Food"]["Amount"].sum()
        return f"Total Food Spending: ₹{total:,.2f}"

    elif "fraud" in query:
        return df[df["ML_Flag"] == "Fraud"]

    elif "total" in query:
        return f"Total Spending: ₹{df['Amount'].sum():,.2f}"

    else:
        return "Try asking about total spending, fraud, or food expenses."
