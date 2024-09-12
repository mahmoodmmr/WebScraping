import sqlite3

# Step 1: Connect to SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect('heroes.db')

# Step 2: Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Step 3: Create the heroes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS heroes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Step 4: Commit changes and close the connection
connection.commit()
connection.close()

print("Database and table created successfully!")

# Step 1: Reconnect to the database
connection = sqlite3.connect('heroes.db')
cursor = connection.cursor()

# Step 2: Insert data
heroes = [('Superman',), ('Batman',), ('Wonder Woman',)]
cursor.executemany('INSERT INTO heroes (name) VALUES (?)', heroes)

# Step 3: Commit changes and close the connection
connection.commit()
connection.close()

print("Heroes inserted successfully!")


# Step 1: Reconnect to the database
connection = sqlite3.connect('heroes.db')
cursor = connection.cursor()

# Step 2: Retrieve data
cursor.execute('SELECT * FROM heroes')
rows = cursor.fetchall()

# Step 3: Print the data
for row in rows:
    print(row)

# Step 4: Close the connection
connection.close()

