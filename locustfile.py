from locust import HttpLocust, TaskSet
from random import randint

signup_url = 'http://0.0.0.0:8000/api/v1/users/signup/'
signin_url = 'http://0.0.0.0:8000/api/v1/users/signin/'


def signup(self):
    x = self.client.post(signup_url, {
        "email": 'tosmahzzky6{0}{1}@gmail.com'.format(randint(1, 100), randint(0, 999)),
        "password": "1717086207H#aAAaaz@@12",
        "first_name": "qq",
        "last_name": "aa"
    })
    print(x.content)


def login(self):
    self.client.post(signin_url, {"email": "tosmak16@gmail.com", "password": "1717086207H#aAAaaz@@12"})


def index(self):
    self.client.get("/")


class UserBehavior(TaskSet):
    tasks = {login: 1, index: 2}

    def on_start(self):
        signup(self)

    def on_stop(self):
        login(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
