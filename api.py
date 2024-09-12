from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('heroes.db')
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

# API to get hero matchups based on the hero name and sorting by best or worst
@app.route('/api/hero-matchups', methods=['GET'])
def get_hero_matchups():
    # Get the query parameters
    hero_name = request.args.get('hero_name')
    variable = request.args.get('variable')  # 'best' or 'worst'
    
    if not hero_name or not variable:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Connect to the database
    conn = get_db_connection()
    
    # Define the query
    if variable == 'best':
        # Get the matchups with the highest win_rate (best matchups)
        query = '''
        SELECT m.*, h.name as opponent_name
        FROM matchup m
        JOIN hero h ON m.heroId = h.id
        WHERE h.name = ?
        ORDER BY m.win_rate DESC
        LIMIT 5
        '''
    elif variable == 'worst':
        # Get the matchups with the lowest win_rate (worst matchups)
        query = '''
        SELECT m.*, h.name as opponent_name
        FROM matchup m
        JOIN hero h ON m.heroId = h.id
        WHERE h.name = ?
        ORDER BY m.win_rate ASC
        LIMIT 5
        '''
    else:
        return jsonify({'error': 'Invalid value for variable. Use "best" or "worst".'}), 400

    # Execute the query
    matchups = conn.execute(query, (hero_name,)).fetchall()
    conn.close()

    # Convert the result into a JSON serializable format
    result = [dict(row) for row in matchups]

    # Return the results
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

