import sqlite3

connection = sqlite3.connect('heroes.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

connection.commit()
connection.close()


connection = sqlite3.connect('heroes.db')
cursor = connection.cursor()
# insert 3 rows into the attributes table
attributes = [('Strength',),('Agility',),('Intelligence',),('Universal',)]
cursor.executemany('INSERT INTO attributes (name) VALUES (?)', attributes)
connection.commit()
connection.close()



# Step 1: Connect to SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect('heroes.db')

# Step 2: Create a cursor object to execute SQL queries
cursor = connection.cursor()
# cursor.execute('''
#                ALTER TABLE heroes
# ADD COLUMN attribute_id INTEGER
# ''')

# Step 3: Create the heroes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS heroes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
    attribute_id INTEGER,
    FOREIGN KEY(attribute_id) REFERENCES attributes(id)
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
heroes = [('abaddon',),
('alchemist',),
('ancient-apparition',),
('anti-mage',),
('arc-warden',),
('axe',),
('bane',),
('batrider',),
('beastmaster',),
('bloodseeker',),
('bounty-hunter',),
('brewmaster',),
('bristleback',),
('broodmother',),
('centaur-warrunner',),
('chaos-knight',),
('chen',),
('clinkz',),
('clockwerk',),
('crystal-maiden',),
('dark-seer',),
('dark-willow',),
('dawnbreaker',),
('dazzle',),
('death-prophet',),
('disruptor',),
('doom',),
('dragon-knight',),
('drow-ranger',),
('earth-spirit',),
('earthshaker',),
('elder-titan',),
('ember-spirit',),
('enchantress',),
('enigma',),
('faceless-void',),
('grimstroke',),
('gyrocopter',),
('hoodwink',),
('huskar',),
('invoker',),
('io',),
('jakiro',),
('juggernaut',),
('keeper-of-the-light',),
('kunkka',),
('legion-commander',),
('leshrac',),
('lich',),
('lifestealer',),
('lina',),
('lion',),
('lone-druid',),
('luna',),
('lycan',),
('magnus',),
('mars',),
('medusa',),
('meepo',),
('mirana',),
('monkey-king',),
('morphling',),
('naga-siren',),
('natures-prophet',),
('necrophos',),
('night-stalker',),
('nyx-assassin',),
('ogre-magi',),
('omn-knight',),
('oracle',),
('outworld-destroyer',),
('pangolier',),
('phantom-assassin',),
('phantom-lancer',),
('phoenix',),
('pr-mirdle-beast',),
('puck',),
('pudge',),
('pugna',),
('queen-of-pain',),
('razor',),
('riki',),
('rubick',),
('sand-king',),
('shadow-demon',),
('shadow-fiend',),
('shadow-shaman',),
('silencer',),
('skywrath-mage',),
('slardar',),
('slark',),
('snapfire',),
('sniper',),
('spectre',),
('spirit-breaker',),
('storm-spirit',),
('sven',),
('techies',),
('templar-assassin',),
('terrorblade',),
('tidehunter',),
('timbersaw',),
('tinker',),
('tiny',),
('treant-protector',),
('troll-warlord',),
('tusk',),
('underlord',),
('undying',),
('ursa',),
('vengeful-spirit',),
('venomancer',),
('viper',),
('visage',),
('void-spirit',),
('warlock',),
('weaver',),
('windranger',),
('winter-wyvern',),
('witch-doctor',),
('wraith-king',),
('zeus',)]
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


connection = sqlite3.connect('heroes.db')
cursor = connection.cursor()

# Step 2: Create the matchup table with a created_at timestamp and hero_id
cursor.execute('''
CREATE TABLE IF NOT EXISTS matchups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hero_id INTEGER NOT NULL,
    hero_name TEXT NOT NULL,
    disadvantage_percentage REAL NOT NULL,
    win_rate REAL NOT NULL,
    matches INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(hero_id) REFERENCES heroes(id)
)
''')

# Step 3: Commit changes and close the connection
connection.commit()
connection.close()



