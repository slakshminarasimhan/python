import streamlit as st
import pandas as pd
import re

# Load CSV data
data_path = "../Output/29Oct2024/rsi/consolidated_rsi.csv"  # Replace with your CSV file path
df = pd.read_csv(data_path)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

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
    # Make a copy of the data for filtering
    filtered_data = data.copy()
    
    # Debug: Print the original DataFrame size
    print("Original DataFrame size:", filtered_data.shape)
    
    # Find all conditions in the query string (e.g., "close > 100" or "14dayrsi > 60")
    matches = re.findall(r'(\b\w+\b)\s*(>|<|>=|<=|==|!=)\s*(\d+)', query.lower())
    print("Parsed conditions:", matches)  # Debug: print parsed conditions
    
    for match in matches:
        column_alias, operator, value = match
        
        # Map the alias to the actual column name
        column_name = columns_map.get(column_alias.lower(), column_alias)
        print(f"Applying filter on column: {column_name}, operator: {operator}, value: {value}")  # Debug

        # Check if the mapped column name exists in the DataFrame
        if column_name in filtered_data.columns:
            value = float(value)  # Convert the value to float for numerical comparison
            
            # Apply filtering based on the operator and print intermediate results
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
            
            # Debug: Print the shape of the DataFrame after each filter is applied
            print(f"DataFrame size after applying {column_name} {operator} {value}:", filtered_data.shape)
        else:
            print(f"Column '{column_name}' not found in DataFrame columns")  # Debug

    # Final debug: Print the resulting DataFrame size and column names
    print("Final filtered DataFrame size:", filtered_data.shape)
    print("Filtered DataFrame columns:", filtered_data.columns)

    return filtered_data

if st.button("Fetch Data"):
    # Check if the user wants a specific date
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', user_query)
    extracted_date = date_match.group(0) if date_match else None

    if extracted_date:
        # Filter data for the specific date
        df = df[df['Date'] == extracted_date]
        print(f"DataFrame size after date filter ({extracted_date}):", df.shape)  # Debug

    # Apply conditions based on the user query
    filtered_df = apply_conditions(df, user_query)

    # Display results
    if not filtered_df.empty:
        st.write("Filtered Data:")
        st.dataframe(filtered_df)
    else:
        st.write("No data found matching the specified conditions.")
