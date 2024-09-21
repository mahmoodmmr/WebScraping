import requests
from bs4 import BeautifulSoup
import json
import certifi
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import sqlite3

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
session.mount('https://', HTTPAdapter(max_retries=retries))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# DB connection
connection = sqlite3.connect('heroes.db')
cursor = connection.cursor()
cursor.execute('SELECT * FROM heroes')
listOfHeros = cursor.fetchall()
connection.close()

# listOfHeros = ["abaddon","alchemist","ancient-apparition","anti-mage","arc-warden","axe","bane","batrider","beastmaster","bloodseeker","bounty-hunter","brewmaster","bristleback","broodmother","centaur-warrunner","chaos-knight","chen","clinkz","clockwerk","crystal-maiden","dark-seer","dark-willow","dawnbreaker","dazzle","death-prophet","disruptor","doom","dragon-knight","drow-ranger","earth-spirit","earthshaker","elder-titan","ember-spirit","enchantress","enigma","faceless-void","grimstroke","gyrocopter","hoodwink","huskar","invoker","io","jakiro","juggernaut","keeper-of-the-light","kunkka","legion-commander","leshrac","lich","lifestealer","lina","lion","lone-druid","luna","lycan","magnus","mars","medusa","meepo","mirana","monkey-king","morphling","naga-siren","nature's-prophet","necrophos","night-stalker","nyx-assassin","ogre-magi","omn-knight","oracle","outworld-destroyer","pangolier","phantom-assassin","phantom-lancer","phoenix","pr-mirdle-beast","puck","pudge","pugna","queen-of-pain","razor","riki","rubick","sand-king","shadow-demon","shadow-fiend","shadow-shaman","silencer","skywrath-mage","slardar","slark","snapfire","sniper","spectre","spirit-breaker","storm-spirit","sven","techies","templar-assassin","terrorblade","tidehunter","timbersaw","tinker","tiny","treant-protector","troll-warlord","tusk","underlord","undying","ursa","vengeful-spirit","venomancer","viper","visage","void-spirit","warlock","weaver","windranger","winter-wyvern","witch-doctor","wraith-king","zeus"]



def insert_matchup(hero_id, hero_name, disadvantage_percentage, win_rate, matches):
    connection = sqlite3.connect('heroes.db')
    cursor = connection.cursor()

    # Step 1: Insert the matchup data into the table
    cursor.execute('''
        INSERT INTO matchups 
        (hero_id, hero_name, disadvantage_percentage, win_rate, matches)
        VALUES (?, ?, ?, ?, ?)
    ''', (hero_id, hero_name, disadvantage_percentage, win_rate, matches))

    # Step 2: Commit the transaction and close the connection
    connection.commit()
    connection.close()

    print(f"Matchup for {hero_name} inserted successfully!")


for hero in listOfHeros:
    print("🚀 ~ hero:", hero[1])
    # response = requests.get(f'https://www.dotabuff.com/heroes/{user}/counters', headers=headers, verify=False)
    # response = requests.get(f'https://www.dotabuff.com/heroes/{user}/counters', headers=headers, verify=certifi.where())
    
    try:
        response = session.get(f'https://www.dotabuff.com/heroes/{hero[4]}/counters', headers=headers, verify=certifi.where())
        print(response.status_code)

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
                # matchup = {
                #     'hero_name': hero_name,
                #     'disadvantage_percentage': disadvantage_percentage,
                #     'win_rate': win_rate,
                #     'matches': matches,
                #     'created_at':datetime.now()
                # }
                
                insert_matchup(hero[0], hero_name, disadvantage_percentage, win_rate, matches)
                
                # Add the matchup to the list
                # matchups.append(matchup)
            
            # Convert the list of matchups to JSON and write to a file
            # with open(f'{hero}.json', 'w', encoding='utf-8') as file:
            #     json.dump(matchups, file, indent=4)
        
            print(f"⚡ Matchup data written to '{hero}.json'")
        else:
            print(" 💀⚡⚡💀 Could not find the table with class 'sortable'")
            
    except requests.exceptions.SSLError as e:
        print(f" 💀⚡⚡💀 SSL Error occurred: {e}")


