from django.urls import reverse
from rest_framework import status

from flight_booking.apps.users.tests.test_auth_base import AuthBase


class UserChangePasswordTest(AuthBase):

    def test_user_change_password_failed_no_password(self):
        """
        User change password fail due to password value not specified
        """

        self.url = reverse('users-detail', kwargs={'id': self.user_id}) + 'change_password/'
        headers = self.headers.copy()
        headers['token'] = self.token
        data = self.user_data.copy()
        response = self.client.patch(self.url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'Password value should have at least 2 uppercase, 2 '
                                                       'lowercase, 2 digit and 2 special character.')

    def test_user_change_password_failed_same_password(self):
        """
        User change password fail due to same new and old password
        """

        self.url = reverse('users-detail', kwargs={'id': self.user_id}) + 'change_password/'
        headers = self.headers.copy()
        headers['token'] = self.token
        data = self.user_data.copy()
        data['password'] = '1234'
        data['old_password'] = '1234'
        response = self.client.patch(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'Current password and new password can not be the same.')

    def test_user_change_password_successful(self):
        """
        User change password successfully
        """

        self.url = reverse('users-detail', kwargs={'id': self.user_id}) + 'change_password/'
        headers = self.headers.copy()
        headers['token'] = self.token
        data = self.user_data.copy()
        data['password'] = '1717086207H#aAAaaz@@12'
        data['old_password'] = '1717086207H#aAAaaz@@12111'
        response = self.client.patch(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'Password updated successfully.')





