from django.urls import reverse
from rest_framework import status

from flight_booking.apps.users.tests.test_auth_base import AuthBase


class UserPasswordResetTest(AuthBase):
    
    def test_user_password_reset_success(self):
        """
        User password reset successful
        """

        self.url = reverse('users-password')
        data = {'email': self.user.email}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'Password reset successful.')

    def test_user_password_reset_failed_no_email(self):
        """
        User password reset failed due no email value
        """

        self.url = reverse('users-password')
        data = {'email': ''}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('message'), 'Account does not exist.')
