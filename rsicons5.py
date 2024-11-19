import pandas as pd
import numpy as np
import os

# Define the RSI calculation function
def calculate_rsi(data, period):
    # Calculate price differences
    delta = data['Close'].diff()
    
    # Separate positive and negative gains
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gains and losses
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    
    # Calculate the RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Consolidate RSI values from multiple CSV files
def consolidate_rsi_from_folder(folder_path, output_file, periods):
    consolidated_data = []

    # Loop through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            data = pd.read_csv(file_path)
            
            # Ensure Date and Close columns are in the expected format
            if 'Date' not in data.columns or 'Close' not in data.columns:
                print(f"Skipping {file_name}: Missing Date or Close column")
                continue

            # Convert Date column to datetime
            data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

            # Calculate rolling RSI for specified periods
            for period in periods:
                data[f'{period}dayrsi'] = calculate_rsi(data, period)
            
            # Add file name as a column
            data['file_name'] = file_name
            
            # Append to the consolidated list
            consolidated_data.append(data)
    
    # Concatenate all data into a single DataFrame
    consolidated_df = pd.concat(consolidated_data, ignore_index=True)
    
    # Save the consolidated DataFrame to a CSV file
    consolidated_df.to_csv(output_file, index=False)
    print(f"Consolidated RSI values saved to {output_file}")

# Specify folder path, output file, and periods
folder_path = "../Output/19Nov2024" 
output_file = "../Output/19Nov2024/rsi/consolidated_rsi.csv"
periods = [14, 21, 34]  # Rolling RSI periods

# Run the consolidation function
consolidate_rsi_from_folder(folder_path, output_file, periods)