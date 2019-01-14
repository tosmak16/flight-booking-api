from django.urls import reverse
from rest_framework import status
from override_storage import override_storage

from flight_booking.apps.users.tests.test_auth_base import AuthBase


@override_storage()
class UserUploadDeletePassportTest(AuthBase):

    def test_user_upload_passport_success(self):
        """
        User passport upload successful
        """

        self.url = reverse('users-passport', kwargs={'id': self.user_id})
        headers = self.headers.copy()
        headers['token'] = self.token
        data = {'passport': 'a.jpg'}
        response = self.client.patch(self.url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'), 'Passport updated successfully.')

    def test_user_upload_failed_no_passport(self):
        """
        User passport upload failed due no passport value
        """

        self.url = reverse('users-passport', kwargs={'id': self.user_id})
        headers = self.headers.copy()
        headers['token'] = self.token
        data = {'passport': ''}
        response = self.client.patch(self.url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'passport field is required.')

    def test_user_delete_success(self):
        """
        User passport delete success
        """

        self.url = reverse('users-passport', kwargs={'id': self.user_id})
        headers = self.headers.copy()
        headers['token'] = self.token
        data = {'passport': ''}
        response = self.client.delete(self.url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data.get('message'), 'Passport deleted successfully.')
