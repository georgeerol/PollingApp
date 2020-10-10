from app import app
import requests
from tests.base_test import BaseTest


class AppTest(BaseTest):

    def test_new_user(self):
        signup_data = {'email': 'user@gmail.com', 'username': 'User',
                       'password': 'password'}
        with app.test_client() as c:
            result = requests.post(self.hostname + '/signup', data=signup_data).text
            self.assertTrue('Thanks for signing up please login' in result)

    def test_login(self):
        # Login data
        data = {'username': 'Administrator', 'password': 'admin'}
        result = self.session.post(self.hostname + '/login', data=data).text
        self.assertTrue('Create a poll' in result)

    def test_empty_option(self):
        json_input = {"title": self.poll['title'],
                      "options": []}
        result = requests.post(self.hostname + '/api/polls', json=json_input).json()
        self.assertEqual('value for options is empty', result['message'])

    def test_new_poll(self):
        result = requests.post(self.hostname + '/api/polls', json=self.poll).json()
        self.assertEqual('Poll was created successfully', result['message'])

    def vote(self):
        input_json = {'poll_title': self.poll['title'],
                      'option': self.poll['options'][0]}
        result = self.session.patch(self.hostname + '/api/poll/vote', input_json).json()
