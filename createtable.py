import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('words.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# SQL command to create the Word table
create_table_query = '''
CREATE TABLE IF NOT EXISTS Word (
    Word VARCHAR(4) PRIMARY KEY,
    Source CHAR(1)
)
'''

# Execute the SQL command to create the table
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'Word' created successfully.")
