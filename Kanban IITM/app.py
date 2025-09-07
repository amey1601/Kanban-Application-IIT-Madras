from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
from datetime import datetime
import json
import random
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# In-memory OTP storage (in production, use Redis or database)
otp_storage = {}

# Database initialization
def init_db():
    conn = sqlite3.connect('kanban.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create lists table with user_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create cards table (list_id already references lists which now have user_id)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            deadline DATE,
            completed BOOLEAN DEFAULT 0,
            list_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (list_id) REFERENCES lists (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('kanban.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(phone, otp):
    # In production, integrate with SMS service like Twilio
    print(f"SMS to {phone}: Your OTP is {otp}")
    return True

def create_default_lists(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    default_lists = ['To Do', 'In Progress', 'Done']
    for list_name in default_lists:
        cursor.execute('INSERT INTO lists (name, user_id) VALUES (?, ?)', (list_name, user_id))
    conn.commit()
    conn.close()

# Authentication Routes
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/forgot-password')
def forgot_password_page():
    return render_template('forgot_password.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    
    if not all([username, email, phone, password]):
        return jsonify({'error': 'All fields are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user already exists
    existing_user = cursor.execute(
        'SELECT id FROM users WHERE username = ? OR email = ? OR phone = ?',
        (username, email, phone)
    ).fetchone()
    
    if existing_user:
        conn.close()
        return jsonify({'error': 'User with this username, email, or phone already exists'}), 400
    
    # Create new user
    password_hash = hash_password(password)
    cursor.execute(
        'INSERT INTO users (username, email, phone, password_hash) VALUES (?, ?, ?, ?)',
        (username, email, phone, password_hash)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Create default lists for new user
    create_default_lists(user_id)
    
    # Set session
    session['user_id'] = user_id
    session['username'] = username
    
    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    conn = get_db_connection()
    password_hash = hash_password(password)
    user = conn.execute(
        'SELECT id, username FROM users WHERE username = ? AND password_hash = ?',
        (username, password_hash)
    ).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    phone = data.get('phone')
    
    if not phone:
        return jsonify({'error': 'Phone number is required'}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT id FROM users WHERE phone = ?', (phone,)).fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'No account found with this phone number'}), 404
    
    # Generate and send OTP
    otp = generate_otp()
    otp_storage[phone] = {
        'otp': otp,
        'user_id': user['id'],
        'timestamp': datetime.now()
    }
    
    if send_otp(phone, otp):
        return jsonify({'message': 'OTP sent successfully'}), 200
    else:
        return jsonify({'error': 'Failed to send OTP'}), 500

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    phone = data.get('phone')
    otp = data.get('otp')
    new_password = data.get('new_password')
    
    if not all([phone, otp, new_password]):
        return jsonify({'error': 'Phone, OTP, and new password are required'}), 400
    
    if phone not in otp_storage:
        return jsonify({'error': 'OTP expired or invalid'}), 400
    
    stored_data = otp_storage[phone]
    if stored_data['otp'] != otp:
        return jsonify({'error': 'Invalid OTP'}), 400
    
    # Check OTP expiry (5 minutes)
    if (datetime.now() - stored_data['timestamp']).seconds > 300:
        del otp_storage[phone]
        return jsonify({'error': 'OTP expired'}), 400
    
    # Update password
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = hash_password(new_password)
    cursor.execute(
        'UPDATE users SET password_hash = ? WHERE id = ?',
        (password_hash, stored_data['user_id'])
    )
    conn.commit()
    conn.close()
    
    # Clean up OTP
    del otp_storage[phone]
    
    return jsonify({'message': 'Password reset successfully'}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

# Middleware to check authentication
def require_auth():
    if 'user_id' not in session:
        return False
    return True

# Main Routes
@app.route('/')
def index():
    if not require_auth():
        return redirect(url_for('login_page'))
    return render_template('index.html', username=session.get('username'))

@app.route('/summary')
def summary_page():
    if not require_auth():
        return redirect(url_for('login_page'))
    return render_template('summary.html', username=session.get('username'))

# API Routes (all require authentication)
@app.route('/api/lists', methods=['GET'])
def get_lists():
    print(f"=== GET LISTS API DEBUG ===")
    print(f"Session: {dict(session)}")
    print(f"User ID: {session.get('user_id')}")
    
    if not require_auth():
        print("❌ Authentication required for lists")
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session['user_id']
    print(f"✅ Authenticated user {user_id}, fetching lists...")
    
    conn = get_db_connection()
    lists = conn.execute(
        'SELECT * FROM lists WHERE user_id = ? ORDER BY id',
        (user_id,)
    ).fetchall()
    
    lists_data = [dict(list_item) for list_item in lists]
    print(f"📋 Found {len(lists_data)} lists for user {user_id}")
    print(f"📋 Lists data: {lists_data}")
    
    # If no lists found, create default ones
    if len(lists_data) == 0:
        print("📝 No lists found, creating default lists...")
        cursor = conn.cursor()
        default_lists = ['To Do', 'In Progress', 'Done']
        created_lists = []
        
        for list_name in default_lists:
            cursor.execute('INSERT INTO lists (name, user_id) VALUES (?, ?)', (list_name, user_id))
            list_id = cursor.lastrowid
            created_lists.append({
                'id': list_id,
                'name': list_name,
                'user_id': user_id,
                'created_at': datetime.now().isoformat()
            })
            print(f"📝 Created list: {list_name} (ID: {list_id})")
        
        conn.commit()
        lists_data = created_lists
        print(f"✅ Created {len(created_lists)} default lists")
    
    conn.close()
    print(f"📤 Returning {len(lists_data)} lists to frontend")
    return jsonify(lists_data)

@app.route('/api/lists', methods=['POST'])
def create_list():
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO lists (name, user_id) VALUES (?, ?)', (name, session['user_id']))
    list_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': list_id, 'name': name}), 201

@app.route('/api/lists/<int:list_id>', methods=['DELETE'])
def delete_list(list_id):
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify list belongs to user
    list_check = cursor.execute(
        'SELECT id FROM lists WHERE id = ? AND user_id = ?',
        (list_id, session['user_id'])
    ).fetchone()
    
    if not list_check:
        conn.close()
        return jsonify({'error': 'List not found'}), 404
    
    # Delete all cards in the list first
    cursor.execute('DELETE FROM cards WHERE list_id = ?', (list_id,))
    # Delete the list
    cursor.execute('DELETE FROM lists WHERE id = ?', (list_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'List deleted successfully'})

@app.route('/api/cards', methods=['GET'])
def get_cards():
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = get_db_connection()
    cards = conn.execute('''
        SELECT c.*, l.name as list_name 
        FROM cards c 
        JOIN lists l ON c.list_id = l.id 
        WHERE l.user_id = ?
        ORDER BY c.created_at DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return jsonify([dict(card) for card in cards])

@app.route('/api/cards', methods=['POST'])
def create_card():
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    title = data.get('title')
    content = data.get('content', '')
    deadline = data.get('deadline')
    list_id = data.get('list_id')
    
    if not title or not list_id:
        return jsonify({'error': 'Title and list_id are required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify list belongs to user
    list_check = cursor.execute(
        'SELECT id FROM lists WHERE id = ? AND user_id = ?',
        (list_id, session['user_id'])
    ).fetchone()
    
    if not list_check:
        conn.close()
        return jsonify({'error': 'List not found'}), 404
    
    cursor.execute('''
        INSERT INTO cards (title, content, deadline, list_id) 
        VALUES (?, ?, ?, ?)
    ''', (title, content, deadline, list_id))
    card_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': card_id, 'title': title, 'content': content, 'deadline': deadline, 'list_id': list_id}), 201

@app.route('/api/cards/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.json
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get current card data and verify ownership
    current_card = cursor.execute('''
        SELECT c.*, l.user_id 
        FROM cards c 
        JOIN lists l ON c.list_id = l.id 
        WHERE c.id = ? AND l.user_id = ?
    ''', (card_id, session['user_id'])).fetchone()
    
    if not current_card:
        conn.close()
        return jsonify({'error': 'Card not found'}), 404
    
    # Update fields
    title = data.get('title', current_card['title'])
    content = data.get('content', current_card['content'])
    deadline = data.get('deadline', current_card['deadline'])
    completed = data.get('completed', current_card['completed'])
    list_id = data.get('list_id', current_card['list_id'])
    
    # If moving to different list, verify new list belongs to user
    if list_id != current_card['list_id']:
        list_check = cursor.execute(
            'SELECT id FROM lists WHERE id = ? AND user_id = ?',
            (list_id, session['user_id'])
        ).fetchone()
        
        if not list_check:
            conn.close()
            return jsonify({'error': 'Target list not found'}), 404
    
    # Set completed_at timestamp if completed status changed
    completed_at = current_card['completed_at']
    if completed and not current_card['completed']:
        completed_at = datetime.now().isoformat()
    elif not completed and current_card['completed']:
        completed_at = None
    
    cursor.execute('''
        UPDATE cards 
        SET title = ?, content = ?, deadline = ?, completed = ?, list_id = ?, 
            updated_at = CURRENT_TIMESTAMP, completed_at = ?
        WHERE id = ?
    ''', (title, content, deadline, completed, list_id, completed_at, card_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Card updated successfully'})

@app.route('/api/cards/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify card belongs to user
    card_check = cursor.execute('''
        SELECT c.id 
        FROM cards c 
        JOIN lists l ON c.list_id = l.id 
        WHERE c.id = ? AND l.user_id = ?
    ''', (card_id, session['user_id'])).fetchone()
    
    if not card_check:
        conn.close()
        return jsonify({'error': 'Card not found'}), 404
    
    cursor.execute('DELETE FROM cards WHERE id = ?', (card_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Card deleted successfully'})

@app.route('/api/summary')
def get_summary():
    if not require_auth():
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = get_db_connection()
    
    # Get overall statistics for current user
    total_cards = conn.execute('''
        SELECT COUNT(*) as count 
        FROM cards c 
        JOIN lists l ON c.list_id = l.id 
        WHERE l.user_id = ?
    ''', (session['user_id'],)).fetchone()['count']
    
    completed_cards = conn.execute('''
        SELECT COUNT(*) as count 
        FROM cards c 
        JOIN lists l ON c.list_id = l.id 
        WHERE c.completed = 1 AND l.user_id = ?
    ''', (session['user_id'],)).fetchone()['count']
    
    pending_cards = total_cards - completed_cards
    
    # Get cards by list for current user
    cards_by_list = conn.execute('''
        SELECT l.name, 
               COUNT(*) as total,
               SUM(CASE WHEN c.completed = 1 THEN 1 ELSE 0 END) as completed
        FROM cards c
        JOIN lists l ON c.list_id = l.id
        WHERE l.user_id = ?
        GROUP BY l.id, l.name
        ORDER BY l.id
    ''', (session['user_id'],)).fetchall()
    
    # Get completion trend (last 7 days) for current user
    completion_trend = conn.execute('''
        SELECT DATE(c.completed_at) as date, COUNT(*) as completed
        FROM cards c
        JOIN lists l ON c.list_id = l.id 
        WHERE c.completed = 1 AND c.completed_at >= date('now', '-7 days') AND l.user_id = ?
        GROUP BY DATE(c.completed_at)
        ORDER BY date
    ''', (session['user_id'],)).fetchall()
    
    # Get overdue cards for current user
    overdue_cards = conn.execute('''
        SELECT COUNT(*) as count
        FROM cards c
        JOIN lists l ON c.list_id = l.id 
        WHERE c.completed = 0 AND c.deadline < date('now') AND l.user_id = ?
    ''', (session['user_id'],)).fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'total_cards': total_cards,
        'completed_cards': completed_cards,
        'pending_cards': pending_cards,
        'overdue_cards': overdue_cards,
        'cards_by_list': [dict(row) for row in cards_by_list],
        'completion_trend': [dict(row) for row in completion_trend]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)