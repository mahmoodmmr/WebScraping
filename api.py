from flask import Flask, request, jsonify
from flask_caching import Cache
import sqlite3
import os

app = Flask(__name__)

# Configure the cache. Here we use the simple cache for demonstration.
# For production, you might want to use a more persistent cache like Redis.
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600  # 1 hour in seconds

cache = Cache(app)

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('heroes.db')
    conn.row_factory = sqlite3.Row  # So we get dict-like row objects
    return conn

# Route to get matchups by hero_id and sort by win rate
@app.route('/matchups', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)  # Cache for 1 hour, based on query string
def get_matchups():
    hero_id = request.args.get('hero_id')
    order = request.args.get('order', 'asc')  # default to ascending order if not provided

    if not hero_id:
        return jsonify({"error": "hero_id is required"}), 400

    # Ensure the sorting order is either asc or desc
    if order not in ['asc', 'desc']:
        return jsonify({"error": "Invalid order. Use 'asc' or 'desc'."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query the matchups table
    query = f'''
        SELECT * FROM matchups
        WHERE hero_id = ?
        ORDER BY win_rate {order}
    '''
    cursor.execute(query, (hero_id,))
    matchups = cursor.fetchall()

    conn.close()

    # If no matchups are found, return a message
    if not matchups:
        return jsonify({"message": "No matchups found for the given hero_id."}), 404

    # Convert the query result to a list of dictionaries
    matchups_list = [dict(row) for row in matchups]

    return jsonify(matchups_list)

# Route to get all heroes
@app.route('/heroes', methods=['GET'])
def get_all_heroes():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to select all heroes from the heroes table
    query = 'SELECT * FROM heroes'
    cursor.execute(query)
    heroes = cursor.fetchall()

    conn.close()

    # If no heroes are found, return a message
    if not heroes:
        return jsonify({"message": "No heroes found."}), 404

    # Convert the query result to a list of dictionaries
    heroes_list = [dict(row) for row in heroes]

    return jsonify(heroes_list)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 12801))
    app.run(host='0.0.0.0', port=port)  # host='0.0.0.0' allows access from the network

