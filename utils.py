def categorize_ai(description):
    desc = description.lower()

    if any(word in desc for word in ["zomato", "swiggy", "restaurant", "cafe"]):
        return "Food"

    elif any(word in desc for word in ["amazon", "flipkart", "mall", "store"]):
        return "Shopping"

    elif any(word in desc for word in ["uber", "ola", "flight", "train"]):
        return "Travel"

    elif any(word in desc for word in ["electricity", "bill", "recharge"]):
        return "Bills"

    else:
        return "Others"
