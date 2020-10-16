from celery import Celery
from flask import (
    Flask, render_template, request, flash, redirect, url_for, session
)
from flask_admin import Admin
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

from admin import AdminView, TopicView
from api.api import api
from db import db
from models import Users, Topics, Polls, Options


def make_celery(app):
    celery = Celery(
        app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


app = Flask(__name__)

app.register_blueprint(api)

app.config.from_object('config')

db.init_app(app)
db.create_all(app=app)

migrate = Migrate(app, db, render_as_batch=True)

# create celery object
celery = make_celery(app)

# admin = Admin(app, name='Dashboard')
# admin.add_view(ModelView(Users, db.session))

admin = Admin(app, name='Dashboard')
admin.add_view(AdminView(Users, db.session))
admin.add_view(AdminView(Polls, db.session))
admin.add_view(AdminView(Options, db.session))
admin.add_view(TopicView(Topics, db.session))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get the user details from the form
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # hash the password
        password = generate_password_hash(password)
        user = Users(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for signing up please login')
        return redirect(url_for('home'))
    # It's a GET request, just render the template
    return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login():
    # we don't need to check the request type as flask will raise a bad request
    # error if a request aside from POST is made to this url
    username = request.form['username']
    password = request.form['password']

    # search the database for the User
    user = Users.query.filter_by(username=username).first()

    if user:
        password_hash = user.password
        if check_password_hash(password_hash, password):
            # The hash matches the password in the database log the user in
            session['user'] = username
            flash('Login was successful')
    else:
        # user wasn't found in the database
        flash('Username or password is incorrect please try again', 'error')
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        flash("we hope to see you again!")
    return redirect(url_for('home'))


@app.route('/polls', methods=['GET'])
def polls():
    return render_template('polls.html')


@app.route('/polls/<poll_name>')
def poll(poll_name):
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
