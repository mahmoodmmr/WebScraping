from flask import Flask, request, jsonify
import sqlite3
# from flask_caching import Cache
import os

app = Flask(__name__)
# cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600})

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('heroes.db')
    conn.row_factory = sqlite3.Row  # So we get dict-like row objects
    return conn

# Route to get matchups by hero_id and sort by win rate
@app.route('/matchups', methods=['GET'])
# @cache.cached()
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

# Initialize database if needed (optional)
# def init_db():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS heroes (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL
#     )
#     ''')
    
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS matchups (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         hero_id INTEGER NOT NULL,
#         hero_name TEXT NOT NULL,
#         disadvantage_percentage REAL NOT NULL,
#         win_rate REAL NOT NULL,
#         matches INTEGER NOT NULL,
#         created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY(hero_id) REFERENCES heroes(id)
#     )
#     ''')
    
#     conn.commit()
#     conn.close()

# Initialize database before the first request (optional)
# @app.before_first_request
# def setup_db():
#     # init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use port from environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)
