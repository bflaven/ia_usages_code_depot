# prompt_traffic_investigation_1.md


## prompt
Read the csv file with Pandas for a file named "sample_1_myexport_20240202112846.csv" with separated columns semi-column ";"

## output


Certainly! You can use the `pandas` library in Python to read a CSV file with semicolon-separated columns. Here's how you can do it:

```python
import pandas as pd

# Assuming the file is in the same directory as your Python script
file_path = "sample_1_myexport_20240202112846.csv"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path, sep=';')

# Display the first few rows of the DataFrame to verify it was read correctly
print(df.head())
```

Make sure to replace `"sample_1_myexport_20240202112846.csv"` with the actual path to your CSV file. The `sep=';'` argument tells pandas to use semicolons as the delimiter when reading the CSV file.

