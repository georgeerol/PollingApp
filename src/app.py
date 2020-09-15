from flask import Flask, render_template
from db import db

app = Flask(__name__)

app.config.from_object('config')

db.init_app(app)
db.create_all(app=app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run()
