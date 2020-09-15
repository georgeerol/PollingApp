from flask import Flask
from db import db

app = Flask(__name__)

app.config.from_object('config')

db.init_app(app)
db.create_all(app=app)


@app.route('/')
def home():
    return 'hello world'


if __name__ == '__main__':
    app.run()
