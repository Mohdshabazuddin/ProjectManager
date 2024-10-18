from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_password', methods=['POST'])
def add_password():
    website = request.json['website']
    password = request.json['password']
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords (website, password) VALUES (?, ?)', (website, password))
    conn.commit()
    conn.close()
    return jsonify({"message": "Password added successfully!"})

@app.route('/get_passwords', methods=['GET'])
def get_passwords():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM passwords')
    passwords = cursor.fetchall()
    conn.close()
    return jsonify([{"id": row[0], "website": row[1], "password": row[2]} for row in passwords])

@app.route('/edit_password/<int:id>', methods=['PUT'])
def edit_password(id):
    new_password = request.json['password']
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE passwords SET password = ? WHERE id = ?', (new_password, id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Password updated successfully!"})

@app.route('/delete_password/<int:id>', methods=['DELETE'])
def delete_password(id):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Password deleted successfully!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
