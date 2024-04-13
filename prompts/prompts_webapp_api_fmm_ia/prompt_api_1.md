# prompt_api_1.md

## prompt
As an advanced programmer in Python, with FastAPI, write an API named "LaylIA", connected to a SQLite database named "data/source.db". The unique endpoint named "write" has the ability to write in a table named "post" of the database.


## output

Sure! Below is an example of how you can create a FastAPI application named "LaylIA" with an endpoint called "write" that allows you to write data to a SQLite database named "data/source.db" in the "post" table:

First, make sure you have FastAPI and SQLite installed in your Python environment. You can install FastAPI using pip:

```bash
pip install fastapi
```

You can use the built-in SQLite3 module for Python which comes pre-installed with Python.

Here's the code:

```python
from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

# Define the path to the SQLite database
DB_PATH = "data/source.db"

# Function to execute SQL queries
def execute_query(query, params=None, fetchone=False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    if fetchone:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

# Endpoint to write data to the 'post' table
@app.post("/write/")
async def write_to_db(content: str):
    query = "INSERT INTO post (content) VALUES (?)"
    try:
        execute_query(query, (content,))
        return {"message": "Data inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

In this code:

- We import the necessary modules.
- We define the path to the SQLite database.
- We create a function `execute_query` to execute SQL queries. This function takes care of establishing a connection to the database, executing the query, and committing the changes.
- We define the endpoint `/write/` using the `@app.post` decorator. This endpoint expects a POST request with JSON data containing the content to be inserted into the database.
- Inside the endpoint function, we execute an SQL `INSERT` query to insert the provided content into the `post` table.

Make sure you have a SQLite database file named `source.db` located inside the `data` directory with a table named `post` defined. You can create the `post` table with the following SQL command:

```sql
CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
);
```

This table has two columns: `id` (auto-incremented primary key) and `content`.