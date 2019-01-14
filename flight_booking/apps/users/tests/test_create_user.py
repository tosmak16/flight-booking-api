from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from flight_booking.apps.users.models import User


class UserCreateTests(APITestCase):

    def setUp(self):
        self.first_user = User.objects.create(
            first_name='first name', email='test@test.com',
            last_name='testpassword', password='testpassword'
        )

        self.second_user = User.objects.create_user(
            email='test2@test.com', password='testpassword2'
        )
        self.user_data = {
            'first_name': 'testfirst',
            'last_name': 'testlast',
            'email': 'test3@test.com',
            'password': 'teST12@#aaAA@@aaaaaaaaa11xx'
        }

        self.url = reverse('users-signup')

    def test_create_account(self):
        """
        Ensure we can create a new user object.
        """
        data = self.user_data.copy()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'), 'you have logged in successfully')

    def test_create_account_failed_invalid_email(self):
        """
        user creation failed when email is invalid
        """
        data = self.user_data.copy()
        data['email'] = 'test'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message').get('email')[0], 'Enter a valid email address.')

    def test_create_account_failed_existing_email(self):
        """
        user creation failed when email already exist
        """
        data = self.user_data.copy()
        data['email'] = 'test2@test.com'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message').get('email')[0], 'user with this email already exists.')

    def test_create_account_failed_no_email(self):
        """
        user creation failed when email is not specified
        """
        data = self.user_data.copy()
        data.pop('email')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message').get('email')[0], 'This field is required.')

    def test_create_account_failed_invalid_password(self):
        """
        user creation failed when password is invalid
        """
        data = self.user_data.copy()
        data['password'] = 'aaAA@@aaaaa'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message').get('password')[0],
                         'Password value should have at least 2 uppercase, 2 lowercase, '
                         '2 digit and 2 special character.')

    def test_create_account_failed_no_password(self):
        """
        user creation failed when password is not specified
        """
        data = self.user_data.copy()
        data.pop('password')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message').get('password')[0], 'This field is required.')

    def test_create_account_failed_no_first_name(self):
        """
        user creation failed when first_name is not specified
        """
        data = self.user_data.copy()
        data.pop('first_name')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message').get('first_name')[0], 'This field is required.')

    def test_create_account_failed_no_last_name(self):
        """
        user creation failed when last_name is not specified
        """
        data = self.user_data.copy()
        data.pop('last_name')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message').get('last_name')[0], 'This field is required.')