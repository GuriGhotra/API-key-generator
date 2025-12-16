from flask import Flask, redirect,  request, render_template, session, url_for
import os
from Database.database import init_db, get_db_conn
from Users.auth import auth
from flask_bcrypt import Bcrypt
from API.apiKey import api_Key
from API.countriesInfo import countries_api
from Users.bcrypt_extension import bcrypt

app = Flask(__name__)

#session management
app.secret_key = os.urandom(24) 

# initialise bcrypt
bcrypt.init_app(app)

# Registration blueprint
app.register_blueprint(auth)
app.register_blueprint(api_Key)
app.register_blueprint(countries_api, url_prefix='/api')


# Initialize database
with app.app_context():
    init_db()

# rendering html
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def singup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    # if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('home'))
    

    # Get user key
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT api_key, created_at, is_active, last_used FROM api_keys WHERE user_id = ? ORDER BY created_at DESC LIMIT 1", (session['user_id'],)
    )
    key_data = cursor.fetchone()
    conn.close()

    return render_template('dashboard.html', username = session.get('username'), api_Key = key_data)


if __name__ == '__main__':
    app.run(debug=True)


