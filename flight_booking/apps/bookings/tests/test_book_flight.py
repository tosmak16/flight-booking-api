from django.urls import reverse
from rest_framework import status

from flight_booking.apps.users.tests.test_auth_base import AuthBase
from flight_booking.apps.bookings.models import Booking


class BookFlightCreateListTest(AuthBase):

    booking_data = dict(
        flight_from='Lagos',
        flight_to='Ekiti',
        flight_type='ROUND',
        owner=1,
        departing_date='2019-07-14',
        returning_date='2019-10-11'
    )
    url = reverse('bookings')

    def test_book_flight_success(self):
        """
        User book flight success
        """

        headers = self.headers.copy()
        headers['token'] = self.token
        data = self.booking_data.copy()
        data['owner'] = self.user_id
        response = self.client.post(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('owner'), data['owner'])
        self.assertEqual(response.data.get('flight_from'), data['flight_from'])
        self.assertEqual(response.data.get('flight_to'), data['flight_to'])
        self.assertEqual(response.data.get('departing_date'), data['departing_date'])
        self.assertEqual(response.data.get('returning_date'), data['returning_date'])
        self.assertEqual(response.data.get('flight_type'), data['flight_type'])

    def test_book_flight_failed_no_returning_date_for_round(self):
        """
        User book flight failed due to no returning date when flight type is ROUND
        """

        headers = self.headers.copy()
        headers['token'] = self.token
        data = self.booking_data.copy()
        data['owner'] = self.user_id
        data.pop('returning_date')
        response = self.client.post(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0], 'returning_date is required.')

    def test_book_flight_failed_invalid_flight_type(self):
        """
        User book flight failed due to invalid flight type
        """

        headers = self.headers.copy()
        headers['token'] = self.token
        data = self.booking_data.copy()
        data['owner'] = self.user_id
        data['flight_type'] = 'TWO'
        response = self.client.post(self.url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('flight_type')[0], 'flight_type can only be ONE or ROUND.')

    def test_get_booked_flights_success(self):
        """
        Admin User get list of booked flight
        """

        headers = self.headers.copy()
        headers['token'] = self.admin_token
        response = self.client.get(self.url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_booked_flights_failed_not_admin_user(self):
        """
        User get list of booked flight failed

        Only Admin user is allowed
        """

        headers = self.headers.copy()
        headers['token'] = self.token
        response = self.client.get(self.url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get('detail'), 'Sorry, you do not have the permission level'
                                                      ' to perform this action.')


class BookFlightUpdateRetrieveTest(AuthBase):

    booking_data = dict(
        flight_from='Lagos',
        flight_to='Ekiti',
        flight_type='ROUND',
        owner=1,
        departing_date='2019-07-14',
        returning_date='2019-10-11'
    )

    def test_update_booked_flight_success(self):
        """
        User update booked flight success
        """
        data = self.booking_data.copy()
        data['owner'] = self.user
        headers = self.headers.copy()
        headers['token'] = self.token
        booked_flight = Booking.objects.create(
            **data
        )
        url_path = '/api/v1/bookings/{0}/'.format(booked_flight.id)
        data.pop('owner')
        response = self.client.put(url_path, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('data').get('flight_from'), data['flight_from'])
        self.assertEqual(response.data.get('data').get('flight_to'), data['flight_to'])
        self.assertEqual(response.data.get('data').get('departing_date'), data['departing_date'])
        self.assertEqual(response.data.get('data').get('returning_date'), data['returning_date'])
        self.assertEqual(response.data.get('data').get('flight_type'), data['flight_type'])

    def test_update_booked_flight_failed_invalid_departing_date(self):
        """
        User update booked flight failed due to invalid departing date
        """
        data = self.booking_data.copy()
        data['owner'] = self.user
        headers = self.headers.copy()
        headers['token'] = self.token
        booked_flight = Booking.objects.create(
            **data
        )
        url_path = '/api/v1/bookings/{0}/'.format(booked_flight.id)
        data.pop('owner')
        data['departing_date'] = '2019-07-141'
        response = self.client.put(url_path, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message').get('departing_date')[0],
                         'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.')

    def test_get_user_booked_flight_success(self):
        """
        User get booked flight success
        """
        data = self.booking_data.copy()
        data['owner'] = self.user
        headers = self.headers.copy()
        headers['token'] = self.token
        booked_flight = Booking.objects.create(
            **data
        )
        url_path = '/api/v1/bookings/{0}/'.format(booked_flight.id)
        response = self.client.get(url_path, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_booked_flight_count_by_date_success(self):
        """
         Test total count of booked flight at a specific date
        """

        data = self.booking_data.copy()
        data['owner'] = self.user
        headers = self.headers.copy()
        headers['token'] = self.token
        Booking.objects.create(
            **data
        )

        url_path = '/api/v1/bookings/users?date={0}'.format(self.booking_data.get('departing_date'))
        response = self.client.get(url_path, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('result'), 1)

    def test_get_booked_flight_count_failed_no_date_in_param(self):
        """
         Get total count of booked flight at a specific date failed due to
         no date in query param
        """

        data = self.booking_data.copy()
        data['owner'] = self.user
        headers = self.headers.copy()
        headers['token'] = self.token
        Booking.objects.create(
            **data
        )

        url_path = '/api/v1/bookings/users'
        response = self.client.get(url_path, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'date is required in the query param.')

    def test_get_booked_flight_count_failed_invalid_date_in_param(self):
        """
         Get total count of booked flight at a specific date failed due to
         invalid date in query param
        """

        data = self.booking_data.copy()
        data['owner'] = self.user
        headers = self.headers.copy()
        headers['token'] = self.token
        Booking.objects.create(
            **data
        )

        url_path = '/api/v1/bookings/users?date={0}'.format('12-01-3333')
        response = self.client.get(url_path, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'),
                         'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.')
