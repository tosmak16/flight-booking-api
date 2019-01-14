from rest_framework.response import Response
from rest_framework import status

from .models import Booking
from .serializers import BookingSerializer


def handle_validate_and_update_booking(request, serialized_book_data, id=None):
    """It handles validate and update booking details

    :param request: contains request data
    :param serialized_book_data: contains serialized booking data
    :param id: booking id
    :return: response message
    """
    if serialized_book_data.is_valid():
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response({'message': 'booking does not exist'}, status=status.HTTP_404_NOT_FOUND)
        booking.flight_from = request.data.get('flight_from') if request.data.get('flight_from') \
            else booking.flight_from
        booking.flight_to = request.data.get('flight_to') if request.data.get('flight_to') else booking.flight_to
        booking.flight_type = request.data.get('flight_type') if request.data.get('flight_type') \
            else booking.flight_type
        booking.departing_date = request.data.get('departing_date') if request.data.get('departing_date') \
            else booking.departing_date
        booking.returning_date = request.data.get('returning_date') if request.data.get('returning_date') \
            else booking.returning_date
        booking.save()
        booking = BookingSerializer(booking).data
        return Response({'message': 'Details updated successfully.', 'data': booking}, status=status.HTTP_200_OK)
    return Response({'message': serialized_book_data.errors}, status=status.HTTP_400_BAD_REQUEST)


