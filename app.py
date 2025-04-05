from flask import Flask, render_template, request, redirect, url_for, session, Response
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import cv2

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MongoDB setup
# client = MongoClient("mongodb+srv://rushikeshnayakavadi:KoppEuYvJKrnXQyI@project1.137egka.mongodb.net/?retryWrites=true&w=majority&ssl=true")
client = MongoClient("mongodb+srv://rushikeshnayakavadi:KoppEuYvJKrnXQyI@project1.137egka.mongodb.net/?retryWrites=true&w=majority&appName=project1")
db = client['driver_sleep']
users_collection = db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match."

        if users_collection.find_one({'email': email}):
            return "Email already exists."

        hashed_pw = generate_password_hash(password)
        users_collection.insert_one({
            'name': name,
            'email': email,
            'password': hashed_pw
        })

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['username'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user_name=session['username'])

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/start-detection', methods=['POST'])
def start_detection():
    if 'username' not in session:
        return redirect(url_for('login'))
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        # detection logic can be added here

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(debug=True)
