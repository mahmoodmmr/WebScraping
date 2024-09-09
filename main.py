import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get('https://www.dotabuff.com/heroes/alchemist/counters', headers=headers, verify=False)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Locate the section containing the table
table = soup.find('table', {'class': 'sortable'})

# List to store matchup data
matchups = []

# Check if the table exists
if table:
    # Find the tbody containing the rows
    tbody = table.find('tbody')
    
    # Loop through each row in the table
    for row in tbody.find_all('tr'):
        # Extract the hero name, disadvantage percentage, win rate, and number of matches
        hero_name = row.find('td', {'class': 'cell-xlarge'}).text.strip()
        disadvantage_percentage = row.find_all('td')[2].text.strip()
        win_rate = row.find_all('td')[3].text.strip()
        matches = row.find_all('td')[4].text.strip()

        # Create a dictionary for each matchup
        matchup = {
            'hero_name': hero_name,
            'disadvantage_percentage': disadvantage_percentage,
            'win_rate': win_rate,
            'matches': matches
        }
        
        # Add the matchup to the list
        matchups.append(matchup)
    
    # Convert the list of matchups to JSON and write to a file
    with open('matchups.json', 'w', encoding='utf-8') as file:
        json.dump(matchups, file, indent=4)

    print("Matchup data written to 'matchups.json'")
else:
    print("Could not find the table with class 'sortable'")
