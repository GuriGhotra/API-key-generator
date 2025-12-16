from flask import Blueprint, request, jsonify, session, url_for, render_template, flash, redirect
from Database.database import get_db_conn
import os
from Users.bcrypt_extension import bcrypt

# bluepritn 
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST', 'GET'])
def register_user():

    
    if request.method == 'POST':
        print("Register form submitted")
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Input validation
        if len(username) < 3:
            flash('Username must be 3 characters')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters')
            return render_template('signup.html')

        # Password hashing
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_conn()
        cursor = conn.cursor()


        try:
            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                flash('Username already exists')
                return render_template('signup.html')
            
            # Check if email exists
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                flash('Email already exists')
                return render_template('signup.html')
            
            # Insert new user - FIXED using cursor
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?,?,?)",
                (username, email, hashed_password)
            )
            conn.commit()
            
            # Get user ID
            user_id = cursor.lastrowid
            
            # Set session
            session['user_id'] = user_id
            session['username'] = username
            
            return redirect(url_for('dashboard'))
        
        except Exception as e:
            conn.rollback()
            flash('Registration failed')
            print(f"Error: {e}")
            return render_template('signup.html')
        
        finally:
            conn.close()
    
    return render_template('signup.html')

# Login Route
@auth.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_conn()
        cursor = conn.cursor()

        # GET user by username
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()


        # Validation
        if user and bcrypt.check_password_hash(user['password'], password):
            # creating session
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return render_template('index.html')
        
    # Getting login page
    return render_template('index.html')


# Logout Route
@auth.route('/logout')
def logout():
    # Clearing session
    session.clear()
    return render_template('index.html')