from flask import Flask
from flask import request
from flask import render_template
from socket import gethostname

app = Flask(__name__)


@app.route('/login', methods=['POST', 'GET'])
@app.route('/hello/')
@app.route('/hello/<name>')

def hello(name=None):
    return render_template('hello.html', name=name)

def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


if __name__ == '__main__':
    # db.create_all()
    if 'liveconsole' not in gethostname():  # Avoid app.run() if deploying on PythonAnywhere service
        app.run(host='127.0.0.1',port=8000,debug=True)
