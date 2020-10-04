"""
BaseTest
This class is be the parent class to each non-unit tests.
It allows for instantiation of the database  dynamically and makes
sure that it is a new, blank database each time
"""

import os
import time
from multiprocessing import Process
from unittest import TestCase
import requests
from app import app, db, celery


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['DEBUG'] = False
        app.config['TESTING'] = True
        cls.DB_PATH = os.path.join(os.path.dirname(__file__), 'votr_test.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(cls.DB_PATH)
        celery.conf.update(CELERY_ALWAYS_EAGER=True)
        cls.hostname = 'http://localhost:7000'
        cls.session = requests.Session()

        with app.app_context():
            db.init_app(app)
            db.create_all()
            cls.p = Process(target=app.run, kwargs={'port': 7000})
            cls.p.start()
            time.sleep(2)

        # create new poll
        poll = {"title": "Flask vs Django",
                "options": ["Flask", "Django"],
                "close_date": 1581556683}
        requests.post(cls.hostname + '/api/polls', json=poll)

        # create new admin user
        signup_data = {'email': 'admin@gmail.com', 'username': 'Administrator',
                       'password': 'admin'}
        requests.post(cls.hostname + '/signup', data=signup_data)

    def setUp(self):
        self.poll = {"title": "who's the fastest footballer",
                     "options": ["Hector bellerin", "Gareth Bale", "Arjen robben"],
                     "close_date": 1581556683}

    @classmethod
    def tearDown(cls):
        os.unlink(cls.DB_PATH)
        cls.p.terminate()
