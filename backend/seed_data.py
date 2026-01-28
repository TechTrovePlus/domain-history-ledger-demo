import sqlite3

def seed():
    conn = sqlite3.connect('backend/dns_guard.db')
    cursor = conn.cursor()

    # Insert a Legitimate Domain
    cursor.execute("INSERT OR IGNORE INTO domains (domain_name, current_status) VALUES (?, ?)", 
                   ('google.com', 'safe'))
    
    # Insert a Known Scam Domain (Our Demo Star)
    cursor.execute("INSERT OR IGNORE INTO domains (domain_name, current_status) VALUES (?, ?)", 
                   ('yourbank-security-update.co', 'malicious'))
    
    # Get the ID of the scam domain
    cursor.execute("SELECT id FROM domains WHERE domain_name = ?", ('yourbank-security-update.co',))
    domain_id = cursor.fetchone()[0]

    # Add an Abuse Event for the scam domain
    cursor.execute('''
        INSERT INTO events (domain_id, event_type, description, integrity_hash)
        VALUES (?, ?, ?, ?)
    ''', (domain_id, 'ABUSE', 'Phishing attempt impersonating a bank', 'temp_hash_123'))

    conn.commit()
    conn.close()
    print("Demo data seeded!")

if __name__ == "__main__":
    seed()