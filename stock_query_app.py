import streamlit as st
import pandas as pd
import re

# Load CSV data
data_path = "../ASIANPAINT.NS.csv"
df = pd.read_csv(data_path)

# User input
user_query = st.text_input("Enter your query (e.g., 'What was the closing price on 2023-12-31?'):")

if st.button("Fetch Data"):
    # Extract column name and date from the query using regular expressions
    column_name_regex = r"(\w+)\s+price"
    date_regex = r"\d{4}-\d{2}-\d{2}"

    column_name_match = re.search(column_name_regex, user_query, re.IGNORECASE)
    date_match = re.search(date_regex, user_query)

    if column_name_match and date_match:
        column_name = column_name_match.group(1)
        date_value = date_match.group()

        # Filter the DataFrame based on the extracted date
        filtered_df = df[df['Date'] == date_value]

        if not filtered_df.empty:
            # Check if the column exists before accessing it
            if column_name in filtered_df.columns:
                value = filtered_df[column_name].values[0]
                st.write(f"The {column_name} on {date_value} is: {value}")
            else:
                st.write(f"The column '{column_name}' does not exist in the data.")
        else:
            st.write("No data found for the specified date.")
    else:
        st.write("Please provide a valid query. Example: 'What was the closing price on 2023-12-31?'")