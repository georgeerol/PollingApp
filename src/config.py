import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')
SECRET_KEY = 'development key'  # keep this key secret during production
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}?check_same_thread=False'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
