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

# Current strategy metrics (buy all captures)
current_success_rate = (df['Gelecek 3 Aylık %'] > 0).mean() * 100
current_avg_return = df['Gelecek 3 Aylık %'].mean()
current_positions = len(df)

print(f"Current Strategy (Buy All Captures):")
print(f"Success Rate: {current_success_rate:.1f}%")
print(f"Number of Positions: {current_positions}")
print(f"Average Return: {current_avg_return:.2f}%\n")

def filter_stocks(stock_row):
    # Count how many times each stock appears
    stock_counts = df['Stock'].value_counts()

    # Create a mask for our filtering conditions
    mask = (
        # Only include stocks that have been captured at least twice
        df['Stock'].map(stock_counts) >= 2
    )

    # Filter the mask with condition
    mask = mask & (
        (df['Gelecek 1 Haftalık %'] >= 2) &
        (df['Gelecek 1 Aylık %'] >= 5) &
        (df['Gelecek 3 Aylık %'] >= 10) &
        (df['Gelecek 6 Aylık %'] >= 20) &
        (df['Gelecek 1 Yıllık %'] >= 40)
    )

    return df[mask]

# Apply the filter
filtered_df = filter_stocks(df)

# Calculate metrics for filtered strategy
filtered_success_rate = (filtered_df['Gelecek 3 Aylık %'] > 0).mean() * 100
filtered_avg_return = filtered_df['Gelecek 3 Aylık %'].mean()
filtered_positions = len(filtered_df)

print(f"Filtered Strategy:")
print(f"Success Rate: {filtered_success_rate:.1f}%")
print(f"Number of Positions: {filtered_positions}")
print(f"Average Return: {filtered_avg_return:.2f}%")
print(f"Reduction in Positions: {((current_positions - filtered_positions)/current_positions)*100:.1f}%")
