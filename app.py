from flask import Flask, request, render_template, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId
import hashlib
from datetime import datetime, timedelta
import os
import jwt
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

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

        if "id" in payload:
            user_info = db.users.find_one({"email": payload["id"]})

            if user_info is not None:
                is_admin = user_info.get("category") == "admin"
                logged_in = True
                print(user_info)
                return render_template('templates_user/home.html', user_info=user_info, logged_in=logged_in, is_admin=is_admin)
            else:
                msg = 'User not found'
                return render_template('templates_user/home.html', msg=msg)

        else:
            msg = 'Invalid token payload'
            return render_template('templates_user/home.html', msg=msg)

    except jwt.ExpiredSignatureError:
        msg = 'Your token has expired'
    except jwt.exceptions.DecodeError:
        msg = 'There was a problem decoding the token'

    return render_template('templates_user/home.html', msg=msg)


@app.route('/home_admin', methods = ['GET'])
def home_admin():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload =jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = db.admin.find_one({"email": payload["id"]})
        # cars = db.cars.find()
        cars = list(db.cars.find())
        is_admin = user_info.get("category") == "admin"
        logged_in = True
        return render_template('templates_admin/home.html', user_info=user_info, cars=cars, logged_in = logged_in, is_admin = is_admin)
    except jwt.ExpiredSignatureError:
        msg = 'Your token has expired'
    except jwt.exceptions.DecodeError:
        msg = 'There was a problem logging you in'
    return render_template('templates_admin/home.html', msg=msg)

@app.route('/signup')
def signup():
    return render_template('/templates_user/register.html')

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

@app.route('/logout')
def logout():
    return render_template('/templates_user/home.html')

@app.route('/syaratketentuan')
def syaratketentuan():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload =jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = db.users.find_one({"email": payload["id"]})
        # cars = db.cars.find()
        # cars = list(db.cars.find())
        is_admin = user_info.get("category") == "admin"
        logged_in = True
        return render_template('/templates_user/syaratketentuan.html', user_info=user_info, logged_in = logged_in, is_admin=is_admin)
    except jwt.ExpiredSignatureError:
        msg = 'Your token has expired'
    except jwt.exceptions.DecodeError:
        msg = 'There was a problem logging you in'
    return render_template('/templates_user/syaratketentuan.html', msg=msg)

@app.route('/carapemesanan')
def carapemesanan():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload =jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = db.users.find_one({"email": payload["id"]})
        # cars = db.cars.find()
        # cars = list(db.cars.find())
        is_admin = user_info.get("category") == "admin"
        logged_in = True
        return render_template('/templates_user/cara_pemesanan.html', user_info=user_info, logged_in = logged_in, is_admin=is_admin)
    except jwt.ExpiredSignatureError:
        msg = 'Your token has expired'
    except jwt.exceptions.DecodeError:
        msg = 'There was a problem logging you in'
    return render_template('/templates_user/cara_pemesanan.html', msg=msg)

@app.route('/about')
def about():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload =jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = db.users.find_one({"email": payload["id"]})
        # cars = db.cars.find()
        # cars = list(db.cars.find())
        is_admin = user_info.get("category") == "admin"
        logged_in = True
        return render_template('/templates_user/about.html', user_info=user_info, logged_in = logged_in, is_admin=is_admin)
    except jwt.ExpiredSignatureError:
        msg = 'Your token has expired'
    except jwt.exceptions.DecodeError:
        msg = 'There was a problem logging you in'
    return render_template('/templates_user/about.html', msg=msg)

@app.route('/contact')
def contact():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload =jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = db.users.find_one({"email": payload["id"]})
        # cars = db.cars.find()
        # cars = list(db.cars.find())
        is_admin = user_info.get("category") == "admin"
        logged_in = True
        return render_template('/templates_user/contact.html', user_info=user_info, logged_in = logged_in, is_admin=is_admin)
    except jwt.ExpiredSignatureError:
        msg = 'Your token has expired'
    except jwt.exceptions.DecodeError:
        msg = 'There was a problem logging you in'
    return render_template('/templates_user/contact.html', msg=msg)
    
@app.route('/contact/save', methods=['POST'])
def contact_save():
    nama = request.form.get('nama')
    email = request.form.get('email')
    phone = request.form.get('phone')
    pesan = request.form.get('pesan')

    doc = {
        "nama": nama,
        "email": email,
        "phone": phone,
        "pesan": pesan
    }
    db.contact.insert_one(doc)
    return render_template('/templates_user/contact.html')

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        judul = request.form.get('judul')
        harga_rental = request.form.get('harga_rental')
        image = request.files['image']

        db.cars.insert_one({
            'judul': judul,
            'harga_rental': harga_rental,
            'image_path': 'path/to/uploaded/image.jpg'
        })
        return redirect(url_for('home_admin'))
    cars = db.cars.find()
    return render_template('templates_admin/add_car.html', cars=cars)


@app.route('/edit_car/<cars_id>', methods=['GET', 'POST'])
def edit_car(cars_id):
    cars = db.cars.find_one({'_id': ObjectId(cars_id)})

    if request.method == 'POST':
        db.cars.update_one(
            {'_id': ObjectId(cars_id)},
            {'$set': {
                'judul': request.form.get('judul'),
                'harga_rental': request.form.get('harga_rental'),
            }}
        )
        return redirect(url_for('home_admin'))

    return render_template('templates_admin/edit_car.html', cars=cars)

@app.route('/delete_car/<cars_id>', methods=['GET', 'POST'])
def delete_car(cars_id):
    cars = db.cars.find_one({'_id': ObjectId(cars_id)})

    if request.method == 'POST':
        db.cars.delete_one({'_id': ObjectId(cars_id)})
        return redirect(url_for('home_admin'))

    return render_template('templates_admin/home.html', cars=cars)

@app.route('/detail')
def detail():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload =jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = db.users.find_one({"email": payload["id"]})
        # cars = db.cars.find()
        # cars = list(db.cars.find())
        is_admin = user_info.get("category") == "admin"
        logged_in = True
        return render_template('/templates_user/detail.html', user_info=user_info, logged_in = logged_in, is_admin=is_admin)
    except jwt.ExpiredSignatureError:
        msg = 'Your token has expired'
    except jwt.exceptions.DecodeError:
        msg = 'There was a problem logging you in'
    return render_template('/templates_user/detail.html', msg=msg)

@app.route('/cek_pesanan/<user_info>')
def cek_pesanan(user_info):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload =jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = db.users.find_one({"email": payload["id"]})
        # cars = db.cars.find()
        # cars = list(db.cars.find())
        is_admin = user_info.get("category") == "admin"
        logged_in = True
        return render_template('/templates_user/cek_pesanan.html', user_info=user_info, logged_in = logged_in, is_admin=is_admin)
    except jwt.ExpiredSignatureError:
        msg = 'Your token has expired'
    except jwt.exceptions.DecodeError:
        msg = 'There was a problem logging you in'
    return render_template('/templates_user/cek_pesanan.html', msg=msg)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
