from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from flight_booking.apps.users.models import User


class UserAuthTests(APITestCase):

    def setUp(self):
        self.first_user = User.objects.create(
            first_name='first name', email='test@test.com',
            last_name='testpassword', password='testpassword'
        )

        self.second_user = User.objects.create_user(
            email='test2@test.com', password='testpassword2'
        )
        self.user_data = {
            'email': 'test2@test.com',
            'password': 'testpassword2'
        }

        self.url = reverse('users-signin')

    def test_user_sign_in_successfully(self):
        """
        User sign in successfully
        """
        data = self.user_data.copy()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'you have logged in successfully')

    def test_user_sign_in_failed_no_registered_email(self):
        """
        User sign in not successfully due to non registered email
        """
        data = self.user_data.copy()
        data['email'] = 'test4@test.co'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('message'), 'email or password is incorrect')

    def test_user_sign_in_failed_invalid_password(self):
        """
        User sign in not successfully due to invalid password
        """
        data = self.user_data.copy()
        data['password'] = 'test4@test.co'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('message'), 'email or password is incorrect')

    def test_user_sign_in_failed_no_email(self):
        """
        user sign in failed when email is not specified
        """
        data = self.user_data.copy()
        data.pop('email')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'email is required.')

    def test_user_sign_in_failed_no_password(self):
        """
        user sign in failed when email is not specified
        """
        data = self.user_data.copy()
        data.pop('password')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'password is required.')