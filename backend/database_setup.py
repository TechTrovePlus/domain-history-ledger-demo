import sqlite3

def init_db():
    conn = sqlite3.connect('backend/dns_guard.db')
    cursor = conn.cursor()

    # 1. Table for general domain info
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_name TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            current_status TEXT DEFAULT 'unknown'
        )
    ''')

    # 2. Table for the History/Audit Log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_id INTEGER,
            event_type TEXT NOT NULL, -- REGISTERED, TRANSFER, ABUSE
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            blockchain_tx TEXT,      -- The Ethereum Transaction Hash
            integrity_hash TEXT,     -- The Keccak-256 fingerprint
            FOREIGN KEY (domain_id) REFERENCES domains (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()