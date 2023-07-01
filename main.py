from flask import Flask, render_template, request, redirect, url_for, jsonify

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


@app.route('/api/token')
def token():
    cookie = request.cookies.get("auth")
    if cookie == '1':
        js = {
            'token': '136576357465'
        }
        return js
    else:
        return redirect(url_for('index'))

@app.route('/api/user')
def api_user():
    cookie = request.cookies.get("auth")
    user = request.cookies.get('name')
    if cookie == '1' and request.args['token'] == '136576357465':
        with open('licensas.txt', 'r') as f:
            _licensas = f.readlines()
            licensas = [i.strip() for i in _licensas]
        return {'user': user, 'licensas': licensas}
    else:
        return redirect(url_for('index'))
