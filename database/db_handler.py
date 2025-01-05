import sqlite3
from datetime import datetime
from security.encryption import load_key, encrypt_password, decrypt_password
from bcrypt import hashpw, gensalt, checkpw

DB_PATH = "password_manager.db"

# Add password function
def add_password(user_id, website, username, password):
    key = load_key()
    encrypted_password = encrypt_password(password, key)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO passwords (user_id, website, username, password, date_added)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, website, username, encrypted_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print(f"Password for {website} added successfully")

# Retrieve password function
def retrieve_passwords(user_id):
    key = load_key()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT website, username, password, date_added FROM passwords WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()

    decrypted_data = []
    for row in rows:
        website, username, encrypted_password, date_added = row
        decrypted_password = decrypt_password(encrypted_password, key)
        decrypted_data.append((website, username, decrypted_password, date_added))

    return decrypted_data

# Register new user function
def register_user(username, password):
    hashed_password = hashpw(password.encode(), gensalt())
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists!")
    conn.close()

# Authenticate existing user
def authenticate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, hashed_password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and checkpw(password.encode(), result[1]):
        return result[0]  
    else:
        return None  

# Update password
def update_password(user_id, old_website, old_username, new_website, new_username, new_password):
    key = load_key()
    encrypted_password = encrypt_password(new_password, key)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE passwords
        SET website = ?, username = ?, password = ?, date_added = ?
        WHERE user_id = ? AND website = ? AND username = ?
    ''', (new_website, new_username, encrypted_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id, old_website, old_username))
    conn.commit()
    conn.close()
    print(f"Password for {old_website} updated successfully")

# Delete password
def delete_password(user_id, website, username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM passwords
        WHERE user_id = ? AND website = ? AND username = ?
    ''', (user_id, website, username))
    conn.commit()
    conn.close()
    print(f"Password for {website} deleted successfully")
