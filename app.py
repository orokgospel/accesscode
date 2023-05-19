from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session encryption

# Create and connect to a SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store user accounts
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                emailaddress TEXT NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                residentkey TEXT NOT NULL
            )''')
conn.commit()

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        emailaddress = request.form['emailaddress']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        residentkey =request.form['residentkey']
        # Validate form data
        if password != confirm_password:
            error_message = "Passwords do not match."
            return render_template('create_account.html', error=error_message)
        
        # Check if username already exists in the database
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        if c.fetchone():
            error_message = "Username already exists."
            return render_template('create_account.html', error=error_message)
        
        # Store user account in the database
        c.execute("INSERT INTO users (username, password, emailaddress,firstname,lastname,residentkey) VALUES (?, ?, ?, ?, ?, ?)", (username, password))
        conn.commit()
        
        # Redirect to login page
        return redirect('/login')
    
    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate form data
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        if not c.fetchone():
            error_message = "Invalid username or password."
            return render_template('login.html', error=error_message)
        
        # Perform user authentication and set session variable
        session['username'] = username
        
        # Redirect to homepage or any other authenticated route
        return redirect('/')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear session variable to indicate user logout
    session.clear()
    
    # Redirect to login page or homepage
    return redirect('/login')

if __name__ == '__main__':
    app.run()
