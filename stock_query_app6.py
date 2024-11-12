import streamlit as st
import pandas as pd
import re

# Load CSV data
data_path = "../Output/29Oct2024/rsi/consolidated_rsi.csv"  # Replace with your CSV file path
df = pd.read_csv(data_path)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# User input
user_query = st.text_input("Enter your query (e.g., 'List companies where 14dayRSI > 60'): ")

# Define a mapping for common column names to ensure flexibility in user queries
columns_map = {
    'close': 'Close',
    'closing': 'Close',
    'opening': 'Open',
    'open': 'Open',
    'high': 'High',
    'low': 'Low',
    'volume': 'Volume',
    '14dayrsi': '14dayRSI',
    '21dayrsi': '21dayRSI',
    '34dayrsi': '34dayRSI'
}

# Function to parse and apply conditions
def apply_conditions(data, query):
    # Initialize an empty list to store conditions
    conditions = []
    
    # Look for conditions in the query using regex for formats like "column > value" or "column < value"
    matches = re.findall(r'(\b\w+\b)\s*(>|<|>=|<=|==|!=)\s*(\d+)', query.lower())
    
    for match in matches:
        column_alias, operator, value = match
        
        # Map the alias to actual column name
        column_name = columns_map.get(column_alias, column_alias)
        
        if column_name in data.columns:
            # Construct the condition string to be used in the query
            conditions.append(f"`{column_name}` {operator} {float(value)}")

    # Combine all conditions into a single query string
    if conditions:
        query_string = " & ".join(conditions)
        filtered_data = data.query(query_string)
        return filtered_data
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no valid conditions

if st.button("Fetch Data"):
    # Check if the user wants a specific date
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', user_query)
    extracted_date = date_match.group(0) if date_match else None

    if extracted_date:
        # Filter data for the specific date
        df = df[df['Date'] == extracted_date]

    # Apply conditions based on the user query
    filtered_df = apply_conditions(df, user_query)

    # Display results
    if not filtered_df.empty:
        st.write("Filtered Data:")
        st.dataframe(filtered_df)
    else:
        st.write("No data found matching the specified conditions.")
