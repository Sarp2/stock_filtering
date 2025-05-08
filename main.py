import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('2007-01-01_2025-04-30_USA_RISK.csv')

# Clean the data - remove rows with no captures
df = df[df['Stock'] != 'No Stocks Captured']

# Convert percentage columns to numeric
return_columns = ['Gelecek 3 Aylık %', 'Gelecek 1 Yıllık %', 'Gelecek 6 Aylık %',
                  'Gelecek 1 Aylık %', 'Gelecek 1 Haftalık %', 'Gelecek 1 Günlük %']
for col in return_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

def filter_stocks(stock_data):
    # Create a list to append the stock information
    results = []

    for _, row in stock_data.iterrows():
        # Buy the stock when captured
        buy_price = row['Güncel Fiyat']
        sell_price = None
        holding_period = None
        return_rate = None

        # Check 1-month return is greater than five percent
        if row['Gelecek 1 Aylık %'] >= 5:
            # If it is, sell the stock and calculate selling price, holding period, and return rate
            sell_price = buy_price * (1 + row['Gelecek 1 Aylık %']/ 100)
            holding_period = '1 month'
            return_rate = row['Gelecek 1 Aylık %']

        # If not, check 3-month return is greater than five percent
        elif row['Gelecek 3 Aylık %'] >= 5:
            # If it is, sell the stock and calculate selling price, holding period, and return rate
            sell_price = buy_price * (1 + row['Gelecek 3 Aylık %']/ 100)
            holding_period = '3 month'
            return_rate = row['Gelecek 3 Aylık %']

        # If not, check 6-month return is greater than five percent
        elif row['Gelecek 6 Aylık %'] >= 5:
            # If it is, sell the stock and calculate selling price, holding period, and return rate
            sell_price = buy_price * (1 + row['Gelecek 6 Aylık %']/ 100)
            holding_period = '6 month'
            return_rate = row['Gelecek 6 Aylık %']

        # If not, check 1-year return is greater than five percent
        elif row['Gelecek 1 Yıllık %'] >= 5:
            # If it is, sell the stock and calculate selling price, holding period, and return rate
            sell_price = buy_price * (1 + row['Gelecek 1 Yıllık %']/ 100)
            holding_period = '1 Yıllık'
            return_rate = row['Gelecek 1 Yıllık %']

        else:
            # If no selling condition met, hold indefinitely (count as negative return)
            sell_price = buy_price
            holding_period  = '>1 year'
            return_rate = 0

        # Append the results to list
        results.append({
            'Date': row['Date'],
            'Stock': row['Stock'],
            'Buy Price': buy_price,
            'Sell Price': sell_price,
            'Holding Period': holding_period,
            'Return %': return_rate,
            'Successful Trade': return_rate >= 5
        })
    return pd.DataFrame(results)

# Create an empty list to collect results of for all stocks
all_trades = []

for stock in df['Stock'].unique():
    # Filters the DataFrame to get only rows for the current stock and sort these rows by date
    stock_data = df[df['Stock'] == stock].sort_values('Date')

    # Apply the filter_stocks function to each stock
    stock_trades = filter_stocks(stock_data)

    # Append it filtered stock to list
    all_trades.append(stock_trades)

# Combine all individual stock DataFrame into one big DataFrame containing all trades
trades_df = pd.concat(all_trades)

# Calculate strategy metrics

# Get the mean of the sucessful Trade and divide by 100
success_rate = trades_df['Successful Trade'].mean() * 100

# Get the mean of the returns
avg_return = trades_df['Return %'].mean()

# Get the length of the trades made by algorithm
num_positions = len(trades_df)

print("Implemented Strategy Results:")
print(f"Success Rate: {success_rate:.1f}%")
print(f"Number of Positions: {num_positions}")
print(f"Average Return: {avg_return:.2f}%")