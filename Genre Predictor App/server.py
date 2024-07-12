from flask import Flask, render_template, session, jsonify
from flask import request, redirect
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
import uuid
from functools import wraps
import predict

server = Flask(__name__)
server.secret_key = b'\xbfo\x07|\xd7\x15\xd1\xbd_\xae)1i\x8b\xab\xd0'
client = MongoClient('localhost', 27017)
db = client.flask_db


@server.route('/', methods=['GET', 'POST'])
def main_page():
    user = request.form
    return render_template('main_page.html', user=user)


@server.route('/signup', methods=['POST'])
def signup():
    print(request.form)
    user = {
        "_id": uuid.uuid4().hex,
        "name": request.form['name'],
        "email": request.form['email'],
        "password": request.form['password'],
        "genres": request.form.getlist('genres')
    }
    print(user)

    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    if db.accounts.find_one({"email": user['email']}):
        return jsonify({"error": "Email address already in use"}), 400

    if db.accounts.insert_one(user):
        print(user)
        return start_session(user)

    return jsonify({"error": "Signup failed"}), 400


def start_session(user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap


@server.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = db.accounts.find_one()
    return render_template('dashboard.html', user=user)


@server.route('/signout', methods=['GET', 'POST'])
def signout():
    session.clear()
    return redirect('/')


@server.route('/login', methods=['POST'])
def login():
    user = db.accounts.find_one({"email": request.form['email']})

    if user and pbkdf2_sha256.verify(request.form['password'], user['password']):
        return start_session(user)

    return jsonify({"error": "Invalid login credentials"}), 401


@server.route('/record', methods=['GET', 'POST'])
def record():
    predict.record_audio()
    genre, tempo, duration = predict.predict_genre()
    print(genre, tempo)
    db.accounts.update_one({"email": session['user']['email']}, {"$push": {"genres": genre}})
    return jsonify({"genre": genre, "tempo": tempo, "duration": duration}), 200


@server.route('/statistics', methods=['GET', 'POST'])
def get_genre_count():
    result = list(db.accounts.aggregate([
        {'$match': {'email': session['user']['email']}},
        {'$unwind': '$genres'},
        {'$group': {'_id': '$genres', 'count': {'$sum': 1}}}
    ]))
    return jsonify(result), 200



if __name__ == "__main__":
    server.run(host="127.0.0.1", port=5001, debug=True)
