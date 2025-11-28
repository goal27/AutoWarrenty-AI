import sqlite3
import json

DATABASE_NAME = 'warranty_checker.db'

def init_db():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                phone_number TEXT,
                address TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS warranties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                extracted_data TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

def add_user(username, password):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Username already exists

def add_user_details(username, password, email=None, phone_number=None, address=None):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, email, phone_number, address) VALUES (?, ?, ?, ?, ?)",
                           (username, password, email, phone_number, address))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Username already exists

def get_user_details(user_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, email, phone_number, address FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return {"username": user[0], "email": user[1], "phone_number": user[2], "address": user[3]}
        return None

def verify_user(username, password):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        return user[0] if user else None

def save_warranty_data(user_id, filename, extracted_data):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO warranties (user_id, filename, extracted_data) VALUES (?, ?, ?)",
                       (user_id, filename, json.dumps(extracted_data)))
        conn.commit()

def get_user_warranties(user_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT filename, extracted_data FROM warranties WHERE user_id = ?", (user_id,))
        warranties = cursor.fetchall()
        return [{'filename': w[0], 'extracted_data': json.loads(w[1])} for w in warranties]

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
