from flask import Flask, request, render_template, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId
import requests
import hashlib
from datetime import datetime
from bson import ObjectId
import os
import jwt
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
from os.path import join, dirname
from dotenv import load_dotenv
from babel.numbers import format_currency

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# MONGODB_URI = os.environ.get("MONGODB_URI")
# DB_NAME =  os.environ.get("DB_NAME")

MONGODB_CONNECTION_STRING = 'mongodb+srv://test_ikakomalasari:sparta@test.nrkvr1l.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.rentcar
# client = MongoClient(MONGODB_URI)
# db = client[DB_NAME]

app = Flask(__name__)

SECRET_KEY = 'secret0'
TOKEN_KEY = 'mytoken'

@app.route('/', methods=['GET'])
def main():
    token_receive = request.cookies.get(TOKEN_KEY)

    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )

        # Check if payload contains the "id" attribute
        if "id" in payload:
            user_info = db.users.find_one({"email": payload["id"]})

            # Check if user_info is not None before accessing its attributes
            if user_info is not None:
                is_admin = user_info.get("category") == "admin"
                logged_in = True
                print(user_info)
                return render_template('templates_user/home.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
            else:
                # Handle the case where user_info is None
                msg = 'User not found'
                return render_template('templates_user/home.html', msg=msg)

        else:
            # Handle the case where "id" is not present in the payload
            msg = 'Invalid token payload'
            return render_template('templates_user/home.html', msg=msg)

    except jwt.ExpiredSignatureError:
        msg = 'Your token has expired'
    except jwt.exceptions.DecodeError:
        msg = 'There was a problem decoding the token'

    return render_template('templates_user/home.html', msg=msg)



@app.route('/home_admin', methods=['GET'])
def home_admin():
    # Fetch card data from the database
    cards = list(db.cards.find())
    return render_template('/templates_admin/home.html', cards=cards)


# ... (existing code)

@app.route('/tambah', methods=['POST'])
def add_card():
    # Get card details from the form
    name = request.form.get('name')
    price = request.form.get('price')
    image = request.form.get('image')

    if not name or not price or not image:
        return jsonify({'result': 'fail', 'msg': 'Please fill in all fields'})

    # Insert card details into the database
    db.cards.insert_one({"name": name, "price": price, "image": image})

    return redirect(url_for('home_admin'))

@app.route('/signup')
def signup():
    return render_template('/templates_user/register.html')

@app.route('/edit_card', methods=['GET'])
def edit_card():
    return render_template('/templates_admin/edit.html') 


@app.route('/delete_card', methods=['POST']) 
def delete_card():
    return jsonify({'result': 'success'})

@app.route('/sign_up/save', methods = ['POST'])
def sign_up():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_hash = hashlib.sha256(password. encode('utf-8')).hexdigest()
    doc = {
        "name" : name,
        "email" : email,
        "category" : 'visitor',
        "password" : password_hash                                          
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/signin')
def signin():
    return render_template('/templates_user/login.html')

@app.route('/sign_in', methods=['POST'])
def sign_in():
    email = request.form["email"]
    password = request.form["password"]
    print(email)
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    print(pw_hash)
    result = db.users.find_one(
        {
            "email": email,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": email,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find a user with that id/password combination",
            }
        )

@app.route('/signup/admin')
def admin_signup():
    return render_template('/templates_admin/admin_register.html')

@app.route('/sign_up/admin', methods=['POST'])
def admin_sign_up():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    doc = {
        "name": name,
        "email": email,
        "category": 'admin', 
        "password": password_hash
    }

    db.admin.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/signin/admin')
def admin_signin():
    return render_template('/templates_admin/admin_login.html')

@app.route('/sign_in/admin', methods=['POST'])
def admin_sign_in():
    admin_email = request.form["email"]
    admin_password = request.form["password"]
    print(admin_email)
    admin_pw_hash = hashlib.sha256(admin_password.encode("utf-8")).hexdigest()
    print(admin_pw_hash)
    result = db.admin.find_one(
        {
            "email": admin_email,
            "password": admin_pw_hash,
            "category": "admin" 
        }
    )
    if result:
        payload = {
            "id": admin_email,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "We could not find an admin with that id/password combination",
            }
        )
    
@app.route('/syaratketentuan')
def syaratketentuan():
    return render_template('/templates_user/syaratketentuan.html')

@app.route('/carapemesanan')
def carapemesanan():
    return render_template('/templates_user/cara_pemesanan.html')

@app.route('/about')
def about():
    return render_template('/templates_user/about.html')

@app.route('/contact')
def contact():
    return render_template('/templates_user/contact.html')
    
@app.route('/contact/save', methods=['POST'])
def contact_save():
    nama = request.form.get('nama')
    email = request.form.get('email')
    pesan = request.form.get('pesan')

    doc = {
        "nama": nama,
        "email": email, 
        "pesan": pesan
    }
    db.contact.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        # Retrieve form data
        judul = request.form.get('judul')
        harga_rental = request.form.get('harga_rental')
        # Add more fields as needed

        # Handle image upload
        image = request.files['image']
        # Process the image (save to a folder, etc.)

        # Insert the car details into the MongoDB database
        db.cars.insert_one({
            'judul': judul,
            'harga_rental': harga_rental,
            # Add more fields as needed
            'image_path': 'path/to/uploaded/image.jpg'  # Update with the actual path
        })

        # Redirect to the admin home page after adding the car
        return redirect(url_for('home_admin'))

    # Render the form for car input
    return render_template('templates_admin/add_car.html')


@app.route('/edit_car/<car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    # Fetch car details from the database using car_id
    car_details = db.cars.find_one({'_id': ObjectId(car_id)})

    # Handle both GET (display form) and POST (update data) requests
    if request.method == 'POST':
        # Update car details in the database
        # ...

        # Redirect to the admin home page after editing the car
        return redirect(url_for('home_admin'))

    # Render a form to edit the car details
    return render_template('templates_admin/edit_car.html', car=car_details)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
