from flask import Blueprint, request, redirect, render_template, flash, url_for
from werkzeug.security import generate_password_hash
from src.database.mongodb_client import MongoDBClient

auth_bp = Blueprint('auth', __name__)
client = MongoDBClient()
db = client.get_database()
users_collection = db["users"]

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # You can implement login logic here
        email = request.form.get('email')
        password = request.form.get('password')
        flash("Login attempted (add real logic)", "info")
        return redirect(url_for('main.home'))

    return render_template('login.html')  # make sure you have login.html


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            flash("User already exists with this email.", "warning")
            return redirect(url_for('auth.signup'))

        # Create new user
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })

        flash("Signup successful. Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('signup.html')
