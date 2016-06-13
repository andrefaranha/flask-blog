from flask import Flask, render_template, request, json
from flask_sqlalchemy import SQLAlchemy


import models


app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    "postgresql://postgres:admin@localhost/flask_blog"
db = SQLAlchemy(app)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    name = request.form['inputName']
    email = request.form['inputEmail']
    password = request.form['inputPassword']

    if name and email and password:
        user = models.User(email, password, name)
        db.session.add(user)
        db.session.commit()

    return json.dumps({'html': '<span>Enter the required fields</span>'})

if __name__ == '__main__':
    app.run()
