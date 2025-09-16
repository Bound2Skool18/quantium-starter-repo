import pandas as pd
import os

# Using a list with all the data files
csv_files = ['data/daily_sales_data_0.csv', 'data/daily_sales_data_1.csv', 'data/daily_sales_data_2.csv']

# Print working directory and check if files exist
print("Current working directory:", os.getcwd())
for file in csv_files:
    print(f"File exists: {file} - {os.path.exists(file)}")

frames = []

for file in csv_files:
    df = pd.read_csv(file)
    print(f"File {file} - Original rows: {len(df)}")
    # Case-insensitive filter for "pink morsel"
    df = df[df['product'].str.lower() == 'pink morsel']
    print(f"File {file} - After filtering: {len(df)}")
    # Remove dollar sign from price before multiplication
    df['sales'] = df['quantity'] * df['price'].str.replace('$', '').astype(float)
    df = df[['sales', 'date', 'region']]
    frames.append(df)

result = pd.concat(frames, ignore_index=True)
print(f"Total rows in result: {len(result)}")
result.to_csv('output.csv', index=False)
print("File saved to output.csv")