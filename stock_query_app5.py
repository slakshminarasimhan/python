import streamlit as st
import pandas as pd
import re

# Load CSV data
data_path = "../ASIANPAINT.NS.csv"
df = pd.read_csv(data_path)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# User input
user_query = st.text_input("Enter your query (e.g., 'What were the closing and opening prices on 2023-12-31?'):")

if st.button("Fetch Data"):
    # Extract date using regex
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', user_query)
    extracted_date = date_match.group(0) if date_match else None

    # Extract columns based on common terms in query
    columns_map = {
        'close': 'Close',
        'closing': 'Close',
        'opening': 'Open',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'volume': 'Volume'
    }

    extracted_columns = []
    for word in user_query.lower().split():
        if word in columns_map:
            extracted_columns.append(columns_map[word])

    # Filter DataFrame for the extracted date and columns
    if extracted_date and extracted_columns:
        filtered_df = df[df['Date'] == extracted_date]

        if not filtered_df.empty:
            for column_name in extracted_columns:
                if column_name in df.columns:
                    value = filtered_df[column_name].values[0]
                    st.write(f"The {column_name} on {extracted_date} is: {value}")
                else:
                    st.write(f"Column '{column_name}' not found in the data.")
        else:
            st.write("No data found for the specified date.")
    else:
        st.write("Could not extract date or column names from the query. Please try again.")
