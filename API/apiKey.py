import secrets
import string
from Database.database import get_db_conn
from flask import Blueprint, session, redirect, url_for, request, jsonify, flash


# Creating BP for the app
api_Key = Blueprint('api_Key', __name__)

# helper fn to generate api keys
def generate_api_key():
    """Generate API key with at least one LC, UC and digit"""
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(10))
        if (any(c.islower() for c in password) and any(c.isupper() for c in password) and sum(c.isdigit() for c in password) >= 3):
            return password
        

@api_Key.route('/generateKey', methods = ['POST'])
def create_key():
    # Checking if user is logged in
    if 'user_id' not in session:
        return jsonify({'error': 'unauthorized'}), 401
    
    user_id = session['user_id']

    conn = get_db_conn()
    cursor = conn.cursor()

    try:
        # Check key already exists for the user
        cursor.execute(
            "SELECT * FROM api_keys WHERE user_id = ? AND is_active = 1", (user_id,)
        )
        existing_key = cursor.fetchone()

        if existing_key:
            flash(" Key already exists. You can disable/enable as needed.", "success")
            return redirect(url_for('dashboard'))

        # Generate new key
        new_key = generate_api_key()

        # Adding new API key
        cursor.execute(
            "INSERT INTO api_keys (user_id, api_key) VALUES (?,?)",
            (user_id, new_key)
        )
        conn.commit()

        flash("API key generated successfuly", "sucess")
        return redirect(url_for('dashboard'))

    except Exception as e:
        conn.rollback()
        flash("Failed to generate key", "error")
        print(f"Error: {e}")
        return redirect(url_for('dashboard'))
    
    finally:
        conn.close()

@api_Key.route('/get_api_key', methods = ['GET'])
def getAPIKey():
    # If user logged in or not

    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    

    user_id = session['user_id']

    conn = get_db_conn()
    cursor = conn.cursor()

    # Get user API key
    cursor.execute(
        "SELECT api_key, created_at, last_used FROM api_keys WHERE user_id = ?", (user_id,)
    )

    key = cursor.fetchone()
    conn.close()

    if key:
        return jsonify({
            'api_key': key['api_key'],
            'created_at': key['created_at'],
            'last_used': key['last_used'] if key['last_used'] else "Not used yet"
        })
    else:
        return jsonify({'error': 'No active API key'}), 404
    


@api_Key.route('/toggleKey', methods=['POST'])
def toggle_key():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    conn = get_db_conn()
    cursor = conn.cursor()
    
    try:
        # Find user's API key
        cursor.execute(
            "SELECT * FROM api_keys WHERE user_id = ?", 
            (user_id,)
        )
        key = cursor.fetchone()
        
        if not key:
            flash("No API key found. Please generate one first.", "error")
            return redirect(url_for('dashboard'))
        
        # Toggle the key status from here
        new_status = 0 if key['is_active'] == 1 else 1
        status_text = "enabled" if new_status == 1 else "disabled"
        
        cursor.execute(
            "UPDATE api_keys SET is_active = ? WHERE id = ?", 
            (new_status, key['id'])
        )
        conn.commit()
        
        flash(f"API key has been {status_text} successfully", "success")
        return redirect(url_for('dashboard'))
    
    except Exception as e:
        conn.rollback()
        flash("Failed to update API key status", "error")
        print(f"Error: {e}")
        return redirect(url_for('dashboard'))
    
    finally:
        conn.close()