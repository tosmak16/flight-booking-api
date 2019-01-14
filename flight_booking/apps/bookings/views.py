import re

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

from .serializers import BookingSerializer, BookingUpdateSerializer
from .models import Booking
from ..users.auth import VerifyToken
from ..users.permissions import GetAdminPermissions, IsOwner
from .helpers import handle_validate_and_update_booking


class BookingsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.CreateModelMixin):
    """ It handles flight bookings operations like booking a flight and getting list of booked flights """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = (VerifyToken,)
    permission_classes = (GetAdminPermissions,)


class BookingsDetailsViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    """ It handles flight bookings operations like getting and updating a booked flight"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = (VerifyToken,)
    permission_classes = (IsOwner,)

    lookup_field = 'id'

    def update(self, request, id=None, *args, **kwargs):
        """It updates bookings details

        :param request: contains request data
        :param id: booking id
        :param args:
        :param kwargs
        :return: response message or data
        """
        serialized_booking_data = BookingUpdateSerializer(data=request.data)
        return handle_validate_and_update_booking(request, serialized_booking_data, id)


@api_view(['GET'])
def users(request):
    date = request.query_params.get('date', None)
    if date is None:
        return Response(
            {'message': 'date is required in the query param.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if re.search(r'(^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$)', date) is None:
        return Response(
            {'message': 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(owner_id) FROM bookings_booking WHERE departing_date = %s", [date])
        database_result = cursor.fetchall()
    if len(database_result):
        for item in database_result[0]:
            result = item

    return Response({'result': result}, status=status.HTTP_200_OK)
