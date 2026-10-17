from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
import sqlite3
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-this-secret')
CORS(app, supports_credentials=True, origins=['http://localhost:5000', 'http://127.0.0.1:5000'])
DB = Path(__file__).parent / 'users.db'

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def initialize():
    with connect() as db:
        db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL)')

@app.get('/')
def home():
    return render_template('index.html')

@app.post('/api/register')
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get('name') or '').strip()
    email = str(data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    if not isinstance(password, str) or not name or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email) or len(password) < 8:
        return jsonify(message='Enter your name, a valid email and a password of at least 8 characters.'), 400
    try:
        with connect() as db:
            db.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)', (name, email, generate_password_hash(password)))
    except sqlite3.IntegrityError:
        return jsonify(message='This email is already registered.'), 409
    return jsonify(message='Account created successfully. You can now log in.'), 201

@app.post('/api/login')
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    if not isinstance(password, str):
        return jsonify(message='Invalid email or password.'), 401
    with connect() as db:
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify(message='Invalid email or password.'), 401
    session.clear()
    session['user_id'] = user['id']
    session['name'] = user['name']
    return jsonify(message='Login successful.', name=user['name'])

@app.get('/api/me')
def me():
    if 'user_id' not in session:
        return jsonify(authenticated=False), 401
    return jsonify(authenticated=True, name=session['name'])

@app.post('/api/logout')
def logout():
    session.clear()
    return jsonify(message='Logged out successfully.')

initialize()
if __name__ == '__main__':
    app.run(debug=True, port=5000)
