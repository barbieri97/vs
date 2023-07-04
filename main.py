from flask import Flask, render_template, request, redirect, url_for, jsonify

from random import randrange

import json

def auth(username, senha):
    data = None
    with open("users.json", "r+") as file:
        _data = json.load(file)
        data = _data.get('users')
    for i in data:
        if i.get('username') == username and i.get('senha') == senha:
            return {"username": username, "tokens": i.get("tokens"), "status": True}
        else:
            return {"status": False}

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        if request.form['user'] == 'admin' and request.form['pass'] == 'pass123':
            resp = redirect('/user')
            resp.set_cookie('auth', '1')
            resp.set_cookie('name', request.form['user'])
            return resp
        else:
            error = 'username or password is wrong'
            return render_template('index.html', error=error)
    else:
        return redirect(url_for('index'))

@app.route('/user')
def user():
    cookie = request.cookies.get("auth")
    user = request.cookies.get('name')
    if cookie == '1':
        with open('licensas.txt', 'r') as f:
            licensas = f.readlines()
        return render_template('user.html', licensas=licensas, user=user)
    else:
        return redirect(url_for('index'))


@app.route('/api/login', methods=["POST"])
def api_login():
    username = request.form.get("username")
    senha = request.form.get("senha")
    l = auth(username, senha)
    if l["status"]:
        return jsonify({"message": "succes", "username": l["username"], "tokens": l["tokens"]})
    else:
        return jsonify({"message": "cant do the login"})

@app.route('/api/buy', methods=['POST'])
def buy():
    username = request.form.get("username")
    senha = request.form.get("senha")
    l = auth(username, senha)
    if l['status']:
        new_token = randrange(100000, 999999)
        with open("users.json", "r+") as file:
            _data = json.load(file)
            data = _data.get('users')
            for i in data:
                if i.get('username') == username and i.get('senha') == senha:
                    i['tokens'].append(new_token)
            _data['users'] = data
            file.truncate(0)
            file.seek(0)
            json.dump(_data, file, indent=4)
            return jsonify(i)
    else:
        return jsonify({'message': "user not found"})

@app.route('/api/pay', methods=['POST'])
def pay():
    username = request.form.get("username")
    senha = request.form.get("senha")
    l = auth(username, senha)
    if l['status']:
        with open("users.json", "r+") as file:
            _data = json.load(file)
            data = _data.get('users')
            for i in data:
                if i.get('username') == username and i.get('senha') == senha:
                    if len(i["tokens"]) == 0:
                        return jsonify({"message": "user has no token"})
                    _ = i['tokens'].pop()
            _data['users'] = data
            file.truncate(0)
            file.seek(0)
            json.dump(_data, file, indent=4)
            return jsonify(i)
    else:
        return jsonify({'message': "user not found"})
    
@app.route('/api/add', methods=["POST"])
def api_add():
    username = request.form.get("username")
    senha = request.form.get("senha")
    l = auth(username, senha)
    if l['status']:
        return jsonify({'message': "user alredy exist"})
    else:
        with open("users.json", "r+") as file:
            _data = json.load(file)
            data = _data.get('users')
            new_user = {"username": username, "senha": senha, "tokens": []}
            data.append(new_user)
            _data['users'] = data
            file.truncate(0)
            file.seek(0)
            json.dump(_data, file, indent=4)
            return jsonify(new_user)