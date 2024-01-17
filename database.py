import sqlite3
from config import DB_PATH

START_WORK_QUERY = '''
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY_KEY, 
    group_number TEXT, 
    email TEXT
);
'''

SEARCH_BY_CHAT_ID_QUERY = '''
SELECT * FROM users WHERE user_id=?
'''

INSERT_CHAT_ID_QUERY = '''
INSERT INTO users (user_id, group_number, email) VALUES (?, ?, ?)
'''

def start_work():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(START_WORK_QUERY)
    conn.commit()
    conn.close()

def check_user_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(SEARCH_BY_CHAT_ID_QUERY, (user_id,))
    res = cursor.fetchone()
    conn.close()
    if res:
        print(res)
        return True
    return False

def insert_user_id(user_id, group_number):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(INSERT_CHAT_ID_QUERY, (user_id, group_number, ""))
    conn.commit()
    conn.close()

def get_group_number(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT group_number FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            group_number = result[0]
            return group_number
        print(f"No entry with User ID = {user_id}")
        return None
    except sqlite3.Error as error:
        print(f"DB' Error: {e}")
    finally:
        conn.close()
