import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('words.db')

# Create a cursor object
cursor = conn.cursor()

# SQL command to select all words from the Word table
select_query = '''
SELECT Word FROM Word where Source = '' order by Word
'''

# Execute the SQL command and fetch all results
cursor.execute(select_query)
words = cursor.fetchall()

# Populate a list with just the words
word_list = [word[0] for word in words]

# Close the connection
conn.close()

print("List of words:", word_list)
