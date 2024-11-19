# MACD (Moving Average Convergence Divergence) and Signal MACD are two related but distinct indicators:
# MACD (Moving Average Convergence Divergence):
# Measures the difference between two EMAs (Exponential Moving Averages):
# Fast EMA (12-period)
# Slow EMA (26-period)
# Indicates the convergence or divergence of the two EMAs
# Crossover points between the two EMAs signal potential buy/sell opportunities
# Signal MACD (Signal Line):
# An EMA (9-period) of the MACD line
# Smooths out the MACD line's fluctuations
# Provides a trigger for buy/sell signals
# Key differences:
# Purpose: MACD measures convergence/divergence, while Signal MACD provides a trigger for signals.
# Calculation: MACD is the difference between two EMAs, while Signal MACD is an EMA of the MACD.
# Sensitivity: MACD is more sensitive to price movements, while Signal MACD is smoother.
# Interpretation:
# Buy signal: MACD crosses above Signal MACD
# Sell signal: MACD crosses below Signal MACD
# Divergence: MACD and price movement diverge (e.g., MACD rises while price falls)

import pandas as pd

# Define MACD calculation function
def calculate_macd(data, short_period, long_period, signal_period):
    # Calculate MACD
    data['ema_short'] = data['Close'].ewm(span=short_period, adjust=False).mean()
    data['ema_long'] = data['Close'].ewm(span=long_period, adjust=False).mean()
    data['macd'] = data['ema_short'] - data['ema_long']
    
    # Calculate Signal MACD
    data['signal_macd'] = data['macd'].ewm(span=signal_period, adjust=False).mean()
    
    return data

# Load input CSV file
input_file = "../Output/19Nov2024/rsi/consolidated_rsi.csv"
output_file = "../Output/19Nov2024/rsi/consolidated_macd.csv"

# Read input CSV file
data = pd.read_csv(input_file)

# Initialize output data
output_data = []

# Loop through each file name
for file_name in data['file_name'].unique():
    file_data = data[data['file_name'] == file_name].copy()  # Add .copy() here
    
    # Calculate MACD and Signal MACD
    file_data = calculate_macd(file_data, 12, 26, 9)
    
    # Fill initial NaN values with 0 (or any other suitable value)
    file_data[['macd', 'signal_macd']] = file_data[['macd', 'signal_macd']].fillna(0)
    
    # Append to output data
    output_data.append(file_data)

# Concatenate output data
output_data = pd.concat(output_data, ignore_index=True)

# Save to output CSV file
output_data.to_csv(output_file, index=False)