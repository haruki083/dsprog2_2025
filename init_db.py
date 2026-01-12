import sqlite3

conn = sqlite3.connect("weather.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_code TEXT,
    area_name TEXT,
    weather TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("DB & weatherテーブル作成完了")
