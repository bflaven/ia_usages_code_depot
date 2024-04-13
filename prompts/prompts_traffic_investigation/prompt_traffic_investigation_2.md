# prompt_traffic_investigation_2.md


## prompt
Create a function that give general information on the number of records from a csv file with Pandas for a file named "sample_1_myexport_20240202112846.csv" with separated columns semi-column ";". Yoiu can leverage on the function below but create a new one named "load_data_infos"

```python
# @st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL, sep=';')
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data
```

## output

To create a function named `load_data_infos` that provides general information about the number of records in a CSV file using Pandas, you can modify the provided function as follows:

```python
import pandas as pd

# Function to load data and provide general information
def load_data_infos(file_path):
    """
    Load data from a CSV file and provide general information.
    
    Parameters:
    - file_path: Path to the CSV file
    
    Returns:
    - df: DataFrame containing the loaded data
    - num_records: Number of records in the DataFrame
    - num_columns: Number of columns in the DataFrame
    """
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path, sep=';')
    
    # Lowercase column names
    df.columns = df.columns.str.lower()
    
    # Get the number of records and columns
    num_records, num_columns = df.shape
    
    # Provide general information
    print("General Information:")
    print(f"Number of Records: {num_records}")
    print(f"Number of Columns: {num_columns}")
    
    return df, num_records, num_columns

# Example usage:
file_path = "sample_1_myexport_20240202112846.csv"
data, num_records, num_columns = load_data_infos(file_path)
```

In this function:
- We load the data from the CSV file using `pd.read_csv`.
- We lowercase the column names using `df.columns.str.lower()`.
- We obtain the number of records and columns in the DataFrame using `df.shape`.
- Finally, we print out the general information and return the DataFrame, number of records, and number of columns.

You can call this function with the path to your CSV file to obtain the desired information.


