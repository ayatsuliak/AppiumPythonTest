import sqlite3


DB_FILE = "results.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_name TEXT,
            date TEXT,
            provider TEXT,
            price TEXT,
            screenshot TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_results(results, hotel_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for date, data in results.items():
        for provider, price in data.get("prices", {}).items():
            cursor.execute("""
                INSERT INTO test_results (hotel_name, date, provider, price, screenshot)
                VALUES (?, ?, ?, ?, ?)
            """, (hotel_name, date, provider, price, data.get("screenshot", "")))

    conn.commit()
    conn.close()


def get_results():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT hotel_name, date, provider, price, screenshot FROM test_results")
    rows = cursor.fetchall()

    conn.close()

    return [{"hotel_name": row[0], "date": row[1], "provider": row[2], "price": row[3], "screenshot": row[4]} for row in
            rows]
