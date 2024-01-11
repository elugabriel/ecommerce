from flask import Flask, render_template, redirect, url_for, request, g, session
from werkzeug.security import check_password_hash
import sqlite3
import bcrypt
import os

app = Flask(__name__)
app.config['DATABASE'] = 'users.db'
app.secret_key = os.urandom(15)

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            state TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_tables()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Convert the user input password to bytes
        password_bytes = password.encode('utf-8')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? OR username = ?', (username, username))
        user = cur.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password_bytes, user['password'].encode('utf-8')):
            # Password is correct, login successful
            session['email'] = user['email']
            session['user_id'] = user['id']
            # Add any other session variables you need

            return redirect(url_for('shop'))  # Redirect to the 'shop' route (you can change it)
        else:
            error = 'Invalid email or password'

    return render_template('login.html', error=error)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


if __name__ == '__main__':
    init_db()  # Initialize the database before running the app
    app.run(debug=True)
