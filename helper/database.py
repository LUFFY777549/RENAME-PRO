import sqlite3
import os

DB_NAME = os.environ.get("DB_NAME", "database.db")   # sqlite file
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
db = conn.cursor()

# table create (Mongo jaise structure banaye rakha)
db.execute("""CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    file_id TEXT
)""")
conn.commit()


def insert(chat_id):
    user_id = int(chat_id)
    try:
        db.execute("INSERT INTO user (id, file_id) VALUES (?, ?)", (user_id, None))
        conn.commit()
    except:
        pass


def addthumb(chat_id, file_id):
    db.execute("UPDATE user SET file_id = ? WHERE id = ?", (file_id, chat_id))
    conn.commit()


def delthumb(chat_id):
    db.execute("UPDATE user SET file_id = NULL WHERE id = ?", (chat_id,))
    conn.commit()


def find(chat_id):
    db.execute("SELECT file_id FROM user WHERE id = ?", (chat_id,))
    data = db.fetchone()
    if data:
        return data[0]


def getid():
    db.execute("SELECT id FROM user")
    values = [row[0] for row in db.fetchall()]
    return values