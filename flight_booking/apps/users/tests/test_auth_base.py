from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from flight_booking.apps.users.helpers import generate_token


class AuthBase(APITestCase):

    def setUp(self):
        self.first_user = get_user_model().objects.create_superuser(
            email='test@test.com', password='testpassword'
        )

        self.second_user = get_user_model().objects.create_user(
            email='test2@test.com', password='testpassword2'
        )
        self.user_data = {
            'email': 'test2@test.com',
            'password': 'testpassword2',
            'first_name': 'testfirst',
            'last_name': 'testlast',
        }

        self.user = get_user_model().objects.get(email='test2@test.com')

        self.user_id = self.user.id

        self.headers = dict(token='aa')

        self.token_exp_date = datetime.now() + timedelta(minutes=5)

        self.token = generate_token(self.user_data.get('email'), self.token_exp_date)
        self.admin_token = generate_token('test@test.com', self.token_exp_date)
