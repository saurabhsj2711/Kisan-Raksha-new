from __future__ import division, print_function
# coding=utf-8
import smtplib,ssl
import sys
import os
import glob
import re
import numpy as np

# Keras
# from keras.applications.imagenet_utils import preprocess_input, decode_predictions
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template, session
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
from smtplib import SMTPException
import MySQLdb.cursors
from werkzeug.utils import secure_filename

# from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)
app.secret_key = 'Kisan Raksha'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Saurabh@123'
app.config['MYSQL_DB'] = 'kisan_raksha'

# Intialize MySQL
mysql = MySQL(app)

# Intialize MySQL
mail = Mail(app)

# Email configurations
app.config['MAIL_DRIVER'] = 'sendmail'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'saurabhsj2711@gmail.com'
app.config['MAIL_PASSWORD'] = 'Saurabh@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Model saved with Keras model.save()
MODEL_PATH = 'model/trained_model.h5'

# Load your trained model
model = load_model(MODEL_PATH)
# Necessary
# print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
# from keras.applications.resnet50 import ResNet50
# model = ResNet50(weights='imagenet')
# model.save('')
print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(150, 150))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    # x = preprocess_input(x, mode='caffe')
    images = np.vstack([x])
    preds = model.predict_classes(images)
    # preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/crops', methods=['GET'])
def crops():
    return render_template('crops.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == "POST":
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "saurabh2711sj@gmail.com"  # Enter your address
        receiver_email = request.form["email"]  # Enter receiver address
        password = "Saurabh@123"
        message = request.form["comments"]

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            print("Sending...")
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            print("Sent")
            return render_template('contact.html')

    # if request.method == "POST":
    #     msg = request.form["comments"]
    #     #subject = "Confirmation Mail"
    #     email = request.form["email"]
    #     print(email,msg)
    #     message = Message(subject="Confirmation Mail",body=msg,sender="saurabhsj2711@gmail.com",recipients=[email])
    #
    #
    #     mail.send(message)
    #     success = "Message sent"
    #     print(success)
    #     return render_template('contact.html')


    return render_template('contact.html')

@app.route('/upload_image', methods=['GET'])
def image_upload():
    return render_template('upload_image.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'mobile' in request.form:
        # Create variables for easy access
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        mobile = request.form['mobile']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE email_id = %s', [email])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z]+', name):
            msg = 'Users Name must contain only characters .!'
        elif not re.match(r'^\d{10}$', mobile):
            msg = 'Invalid Mobile Number'
        elif not name or not password or not email or not mobile:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user_details VALUES (NULL, %s, %s, %s,%s)', [name, mobile, email, password])
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return render_template('log_in.html', msg=msg)
            # return here where you want to redirect
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE email_id = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['uid']
            session['username'] = account['name']
            # Redirect to home page after login
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('crops.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #old_user = session['username']
    session.pop('username', None)
    session.pop('id', None)
    session['loggedin'] = False
    #flash('Looks like '+old_user+' have logged out!')
    return redirect(url_for(''))


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        print("upload")
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'upload', secure_filename(f.filename))
        f.save(file_path)
        print("Image uploaded")

        # Make prediction
        preds = model_predict(file_path, model)
        print(preds[0])

        l = ["Not identified", "Alternaria", "Bacterial Blight", "Chlororsis", "Grey Mildew","healthy"]
        result = l[preds[0]]

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        # result = str(pred_class[0][0][1])               # Convert to string
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
