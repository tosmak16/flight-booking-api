from locust import HttpLocust, TaskSet
from random import randint

signup_url = 'http://0.0.0.0:8000/api/v1/users/signup/'
signin_url = 'http://0.0.0.0:8000/api/v1/users/signin/'
bookings = 'http://0.0.0.0:8000/api/v1/bookings/'

fake_number = 51


def signup(self):
    self.client.post(signup_url, {
        "email": 'tosmahzzky6{0}{1}@gmail.com'.format(randint(1, 1000), randint(0, 9999)),
        "password": "1717086207H#aAAaaz@@12",
        "first_name": "qq",
        "last_name": "aa"
    })


def book(self):
    self.client.post(signup_url, {
        "flight_from": "Lagos",
        "flight_to": "Abuja",
        "flight_type": "ONE",
        "owner": fake_number
    })


def login(self):
    self.client.post(signin_url, {"email": "tosmak16@gmail.com", "password": "1717086207H#aAAaaz@@12"})


class UserBehavior(TaskSet):
    tasks = {login: 1, book: 2}

    def on_start(self):
        signup(self)

    def on_stop(self):
        login(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
