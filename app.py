import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Уязвимость: потенциальное извлечение данных без аутентификации
    cursor.execute("SELECT id, username, email FROM users")
    users = [{"id": row[0], "username": row[1], "email": row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    username = data.get('username', '')
    email = data.get('email', '')

    # SAST Warning (Bandit B307): Уязвимость eval
    # Намерено добавлено для демонстрации SAST сканирования
    if username.startswith("eval:"):
        eval(username.split("eval:")[1])

    # DAST Warning / OWASP Top 10 (A03: Injection): SQL Injection via raw string formatting
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"INSERT INTO users (username, email) VALUES ('{username}', '{email}')"
    cursor.executescript(query)
    conn.commit()
    conn.close()

    return jsonify({"message": "User created successfully", "username": username}), 201

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # DAST Warning (A01: Broken Access Control): Отсутствует авторизация на удаление
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"User {user_id} deleted"}), 200

if __name__ == '__main__':
    # B104: Hardcoded bind to all interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)