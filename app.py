# app.py

from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

# Your existing imports
import numpy as np
from keras.models import load_model
import pydicom
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model
model = load_model('trained_model2.h5')
model.compile(optimizer='adam', 
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Function to preprocess DICOM images
def preprocess_dicom(file):
    ds = pydicom.dcmread(file)
    img = ds.pixel_array.astype(float)
    img /= np.max(img)  # Normalize pixel values
    img = np.expand_dims(img, axis=(0, -1))  # Add batch and channel dimensions
    return img

# Function to preprocess uploaded images
def preprocess_image(file):
    img = Image.open(io.BytesIO(file.read()))
    img = img.convert('L')  # Convert to grayscale
    img = img.resize((512, 512))  # Resize to match model input shape
    img_array = np.array(img)
    img_array = img_array / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=(0, -1))  # Add batch and channel dimensions
    return img_array

# Route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the uploaded file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part detected'}), 400
    file = request.files['file']

    # Preprocess the DICOM image
    #try:
        #image = preprocess_dicom(file)
    #except Exception as e:
        #return jsonify({'error': str(e)}), 400
    #image = preprocess_dicom(file)
    image = preprocess_image(file)
    # Make predictions
    predictions = model.predict(image)

    # Format predictions
    fracture_probability = float(predictions[0][0])
    c1c7_probabilities = predictions[1][0].tolist()

    # Return predictions
    return jsonify({
        'fracture_probability': fracture_probability,
        'c1c7_probabilities': c1c7_probabilities
    })

# Route for sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return 'Username already exists. <a href="/login">Login</a>'
        
        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the SQLite database
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        
        # Check if the username and password match
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    
    return render_template('login.html')

# Route for index page
@app.route('/index')
def index():
    return render_template('index.html')

# Route for logout
@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
