from flask import Flask, render_template, request, redirect, url_for, session, Response
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MongoDB setup
# client = 
client = MongoClient("mongodb+srv://rushikeshnayakavadi:KoppEuYvJKrnXQyI@project1.137egka.mongodb.net/?retryWrites=true&w=majority&appName=project1")
db = client['driver_sleep']
users_collection = db['users']

# Load the trained model
model = load_model('models/sleep_detection_model.h5')
print("[DEBUG] Model Input Shape:", model.input_shape)

# Class labels (same order used during training)
class_labels = ['Closed', 'Open', 'Yawn', 'No_Yawn']


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


# Function to predict a single frame
from playsound import playsound
import threading
import os

# Play sound in background to avoid blocking video stream
def play_alarm():
    threading.Thread(target=playsound, args=(os.path.join("static", "sounds", "alarm.mp3"),), daemon=True).start()

# Updated predict_frame function
def predict_frame(frame):
    try:
        print("[DEBUG] Received frame of shape:", frame.shape)

        resized = cv2.resize(frame, (64, 64))
        print("[DEBUG] Resized frame shape:", resized.shape)

        normalized = resized / 255.0
        input_data = normalized.reshape(1, 64, 64, 3)
        print("[DEBUG] Reshaped input for model:", input_data.shape)

        predictions = model.predict(input_data)
        print("[DEBUG] Predictions:", predictions)

        predicted_class = class_labels[np.argmax(predictions)]
        print("[DEBUG] Predicted Class:", predicted_class)

        # 🔊 Play alarm for "Closed" or "Yawn"
        if predicted_class in ['Closed', 'Yawn']:
            play_alarm()

        return predicted_class

    except Exception as e:
        print("[ERROR in predict_frame()]:", e)
        return "Error"

# Frame generator function
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        label = predict_frame(frame)

        # Draw the label on the frame
        cv2.putText(frame, f"Status: {label}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(debug=True)
