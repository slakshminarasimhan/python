import streamlit as st
import pandas as pd
import re
import os
import time
from pathlib import Path

# Configuration for the comments directory
comments_dir = "../Output/Comments"  # Set your desired directory path here
Path(comments_dir).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

# Load CSV data
data_path = "../Output/29Oct2024/rsi/consolidated_rsi.csv"  # Replace with your CSV file path
df = pd.read_csv(data_path)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Initialize session state for filtered data and comments
if "filtered_df" not in st.session_state:
    st.session_state["filtered_df"] = None
if "user_comments" not in st.session_state:
    st.session_state["user_comments"] = ""

# User input
user_query = st.text_input("Enter your query (e.g., 'Close > 1000 and 14dayrsi > 60'): ")

# Define a mapping for common column names to ensure flexibility in user queries
columns_map = {
    'close': 'Close',
    'closing': 'Close',
    'opening': 'Open',
    'open': 'Open',
    'high': 'High',
    'low': 'Low',
    'volume': 'Volume',
    '14dayrsi': '14dayrsi',  # Ensure lowercase "rsi"
    '21dayrsi': '21dayrsi',
    '34dayrsi': '34dayrsi'
}

# Function to parse and apply conditions without relying on pandas.query()
def apply_conditions(data, query):
    filtered_data = data.copy()
    print("Initial DataFrame size:", filtered_data.shape)  # Debug: Print the initial size

    # Parse and apply filters
    matches = re.findall(r'(\b\w+\b)\s*(>|<|>=|<=|==|!=)\s*(\d+)', query.lower())
    for match in matches:
        column_alias, operator, value = match
        column_name = columns_map.get(column_alias.lower(), column_alias)

        if column_name in filtered_data.columns:
            value = float(value)
            print(f"Filtering: {column_name} {operator} {value}")  # Debug: Print filter details

            # Apply filtering based on the operator
            if operator == '>':
                filtered_data = filtered_data[filtered_data[column_name] > value]
            elif operator == '<':
                filtered_data = filtered_data[filtered_data[column_name] < value]
            elif operator == '>=':
                filtered_data = filtered_data[filtered_data[column_name] >= value]
            elif operator == '<=':
                filtered_data = filtered_data[filtered_data[column_name] <= value]
            elif operator == '==':
                filtered_data = filtered_data[filtered_data[column_name] == value]
            elif operator == '!=':
                filtered_data = filtered_data[filtered_data[column_name] != value]

            print("DataFrame size after filtering:", filtered_data.shape)  # Debug: Print size after filter
        else:
            print(f"Column '{column_name}' not found in DataFrame columns")  # Debug: Log missing column

    print("Final filtered DataFrame size:", filtered_data.shape)  # Debug: Print final size
    return filtered_data


# Button to trigger filtering
if st.button("Fetch Data"):
    # Check if the user wants a specific date
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', user_query)
    extracted_date = date_match.group(0) if date_match else None

    if extracted_date:
        # Filter data for the specific date
        df = df[df['Date'] == extracted_date]
        print(f"DataFrame size after date filter ({extracted_date}):", df.shape)  # Debug: Log size after date filter

    # Apply conditions based on the user query
    filtered_df = apply_conditions(df, user_query)

    # Store the filtered data in session state
    st.session_state["filtered_df"] = filtered_df

# Check if filtered data is available
if st.session_state["filtered_df"] is not None:
    filtered_df = st.session_state["filtered_df"]

    # Display the filtered data
    st.write(f"Filtered Data (Rows: {filtered_df.shape[0]}):")
    st.dataframe(filtered_df)

    # Generate a timestamp for the filename suffix
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Button to download filtered data with a timestamped filename
    csv_data = filtered_df.to_csv(index=False, encoding='utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"filtered_data_{timestamp}.csv",
        mime="text/csv"
    )

    # Text area for comments
    user_comments = st.text_area("Add your comments (optional):", value=st.session_state["user_comments"])

    # Save comments button
    if st.button("Save Comments"):
        # Update session state for comments
        st.session_state["user_comments"] = user_comments

        # Save comments to the configured directory with a timestamped filename
        comments_file_path = os.path.join(comments_dir, f"user_comments_{timestamp}.txt")

        # Write comments to the file
        with open(comments_file_path, "w", encoding="utf-8") as comments_file:
            comments_file.write(user_comments.strip())

        st.success(f"Comments saved to {comments_file_path}")
