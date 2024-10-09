const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const NodeCache = require('node-cache');
const app = express();
const port = process.env.PORT || 12801;

// Configure the cache
const cache = new NodeCache({ stdTTL: 3600 }); // 1 hour in seconds

// Function to get a database connection
const getDbConnection = () => {
    return new sqlite3.Database('heroes.db', (err) => {
        if (err) {
            console.error('Could not connect to database', err);
        }
    });
};

// Route to get all heroes
app.get('/heroes', (req, res) => {
    const db = getDbConnection();
    
    // Query the heroes table
    const query = `SELECT * FROM heroes`;
    
    db.all(query, [], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: 'Database error' });
        }

        // If no heroes are found, return a message
        if (rows.length === 0) {
            return res.status(404).json({ message: 'No heroes found.' });
        }

        // Convert the query result to a list of objects
        const heroesList = rows.map(row => {
            return {
                id: row.id, // Adjust based on your actual column names
                name: row.name,
                // Add other fields as necessary
            };
        });

        return res.json(heroesList);
    });

    db.close();
});

// Route to get matchups by hero_id and sort by win rate
app.get('/matchups', (req, res) => {
    const heroId = req.query.hero_id;
    const order = req.query.order || 'asc'; // default to ascending order if not provided

    if (!heroId) {
        return res.status(400).json({ error: 'hero_id is required' });
    }

    // Ensure the sorting order is either asc or desc
    if (!['asc', 'desc'].includes(order)) {
        return res.status(400).json({ error: "Invalid order. Use 'asc' or 'desc'." });
    }

    // Check cache
    const cacheKey = `matchups_${heroId}_${order}`;
    const cachedMatchups = cache.get(cacheKey);

    if (cachedMatchups) {
        return res.json(cachedMatchups);
    }

    const db = getDbConnection();
    
    // Query the matchups table
    const query = `
        SELECT * FROM matchups
        WHERE hero_id = ?
        ORDER BY win_rate ${order}
    `;
    
    db.all(query, [heroId], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: 'Database error' });
        }

        // If no matchups are found, return a message
        if (rows.length === 0) {
            return res.status(404).json({ message: 'No matchups found for the given hero_id.' });
        }

        // Convert the query result to a list of objects
        const matchupsList = rows.map(row => {
            return {
                id: row.id, // Adjust based on your actual column names
                hero_id: row.hero_id,
                win_rate: row.win_rate,
                // Add other fields as necessary
            };
        });

        // Cache the result
        cache.set(cacheKey, matchupsList);

        return res.json(matchupsList);
    });

    db.close();
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://0.0.0.0:${port}`);
});
