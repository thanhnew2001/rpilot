import pandas as pd

# Read data from CSV file
csv_file = "datesensorasrows_eav.csv"
df = pd.read_csv(csv_file)

# Select columns to transpose
columns_to_transpose = ['Sensor']

# Transpose selected columns
transposed_columns = df[columns_to_transpose].T

# Print the original and transposed columns
print("Original DataFrame:")
print(df)
print("\nTransposed Columns:")
print(transposed_columns)
