import pdfplumber
import pandas as pd
import re

def extract_pdf_data_advanced(file):
    data = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                pattern = r'(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(-?\d+,\d+\.\d+|\d+\.\d+)'
                matches = re.findall(pattern, text)

                for match in matches:
                    date = match[0]
                    description = match[1]
                    amount = float(match[2].replace(",", ""))
                    data.append([date, description, amount])

    return pd.DataFrame(data, columns=["Date", "Description", "Amount"])
