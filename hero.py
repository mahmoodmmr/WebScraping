import sqlite3
from bs4 import BeautifulSoup

# Parse HTML content from the file
with open('./Untitled-1.html', 'r') as file:

    content = file.read()

soup = BeautifulSoup(content, 'html.parser')

# Create SQLite connection
conn = sqlite3.connect('heroes.db')
cursor = conn.cursor()

# Create table for heroes with an image column
cursor.execute('''CREATE TABLE IF NOT EXISTS heroes
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              attribute TEXT,
              image_url TEXT)''')

# Commit the changes and close the connection
conn.commit()
conn.close()

conn = sqlite3.connect('heroes.db')
c = conn.cursor()

# Find the hero attributes (e.g., Strength, Agility, Intelligence)
attributes_sections = soup.find_all('div', class_='tw-mb-3')

for section in attributes_sections:
    # Get the attribute (Strength, Agility, Intelligence)
    attribute_name = section.find('div', class_='tw-font-semibold').get_text().strip()

    # Find all heroes within this section
    heroes_div = section.find_next_sibling('div')
    hero_links = heroes_div.find_all('a', class_='tw-group')

    for hero in hero_links:
        # Get hero name
        hero_name = hero.find('div', class_='tw-leading-none').get_text().strip()
        
        # Get image URL
        hero_image = hero.find('img')
        image_url = hero_image['src'].strip() if hero_image else None
        
        # Insert hero data into the SQLite database
        c.execute("INSERT INTO heroes (name, attribute, image_url) VALUES (?, ?, ?)", 
                  (hero_name, attribute_name, image_url))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Hero data including images has been successfully inserted into the database.")
