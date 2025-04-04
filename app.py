from flask import Flask, render_template, request, redirect, url_for, session, Response
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import cv2


app = Flask(__name__)
app.secret_key = "your_secret_key"  

from src.routes.auth_routes import auth_bp

app.register_blueprint(auth_bp)

from src.routes.main_routes import main_bp
app.register_blueprint(main_bp)



# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['driver_sleep']
users_collection = db['users']

# -------------------- ROUTES --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        if users_collection.find_one({'username': username}):
            return "Username already exists. Try a different one."

        hashed_pw = generate_password_hash(password)
        users_collection.insert_one({'username': username, 'password': hashed_pw})

        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
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

# -------------------- WEBCAM DETECTION ROUTES --------------------

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

        # you can run your detection logic here

        # encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# -------------------- MAIN --------------------

if __name__ == '__main__':
    app.run(debug=True)
