import yfinance as yf
import os

# List of NIFTY 50 symbols
# nifty_50_symbols = [
#     "ADANIPORTS.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS",
#     "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS", "INFRATEL.NS", "BRITANNIA.NS",
#     "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS", "GAIL.NS", "GRASIM.NS",
#     "HCLTECH.NS", "HDFCBANK.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS",
#     "HDFC.NS", "ICICIBANK.NS", "ITC.NS", "IOC.NS", "INDUSINDBK.NS", "INFY.NS",
#     "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", "M&M.NS", "MARUTI.NS", "NTPC.NS",
#     "NESTLEIND.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBIN.NS", "SHREECEM.NS",
#     "SUNPHARMA.NS", "TCS.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS",
#     "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "VEDL.NS", "WIPRO.NS", "YESBANK.NS",
#     "ZEEL.NS"
# ]

nifty_50_symbols = [
    "ASIANPAINT.NS"
]


# Create a directory to store the CSV files if it doesn't exist
output_directory = "C:\\Laks\\Projects\\Python\\Finance\\nse"
os.makedirs(output_directory, exist_ok=True)

# Fetching data for each symbol and saving to CSV
for symbol in nifty_50_symbols:
    try:
        data = yf.download(symbol, start="2000-01-01")
        output_file = os.path.join(output_directory, f"{symbol}.csv")
        data.to_csv(output_file)
        print(f"Data for {symbol} has been saved to {output_file}")
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
