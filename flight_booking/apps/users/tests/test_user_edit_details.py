from django.urls import reverse
from rest_framework import status
from datetime import datetime, timedelta

from flight_booking.apps.users.helpers import generate_token
from flight_booking.apps.users.tests.test_auth_base import AuthBase


class UserDetailTest(AuthBase):

    def test_user_update_failed_no_token(self):
        """
        User update failed due to no token.
        """
        self.url = reverse('users-detail', kwargs={'id': self.user_id})
        headers = self.headers.copy()
        headers.pop('token')
        data = self.user_data.copy()
        response = self.client.put(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Token is required.')

    def test_user_update_failed_invalid_token(self):
        """
        User update failed due to invalid token.
        """
        self.url = reverse('users-detail', kwargs={'id': self.user_id})
        headers = self.headers.copy()
        data = self.user_data.copy()
        response = self.client.put(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Authorization failed due to an Invalid token.')

    def test_user_update_failed_expired_token(self):
        """
        User update failed due to expired token.
        """
        self.url = reverse('users-detail', kwargs={'id': self.user_id})
        headers = self.headers.copy()
        token_exp_date = datetime.now() - timedelta(minutes=5)
        headers['token'] = generate_token(self.user_data.get('email'), token_exp_date )
        data = self.user_data.copy()
        response = self.client.put(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Token has expired.')

    def test_user_update_successful(self):
        """
        User update successful
        """

        self.url = reverse('users-detail', kwargs={'id': self.user_id})
        headers = self.headers.copy()
        headers['token'] = self.token
        data = self.user_data.copy()
        response = self.client.put(self.url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'Details updated successfully.')
        self.assertEqual(response.data.get('data').get('id'), self.user_id)
        self.assertEqual(response.data.get('data').get('first_name'), data.get('first_name'))
        self.assertEqual(response.data.get('data').get('last_name'), data.get('last_name'))

    def test_user_partial_update_successful(self):
        """
        User partial update successful
        """

        self.url = reverse('users-detail', kwargs={'id': self.user_id})
        headers = self.headers.copy()
        headers['token'] = self.token
        data = self.user_data.copy()
        data.pop('email')
        data.pop('password')
        data.pop('last_name')
        response = self.client.patch(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'Details updated successfully.')
        self.assertEqual(response.data.get('data').get('id'), self.user_id)
        self.assertEqual(response.data.get('data').get('first_name'), data.get('first_name'))



