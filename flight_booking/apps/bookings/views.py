import re

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection


from .serializers import BookingSerializer
from .models import Booking
from ..users.auth import VerifyToken
from ..users.permissions import GetAdminPermissions, IsOwner


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


@api_view(['GET'])
def users(request):
    date = request.query_params.get('date', None)
    if date is None:
        return Response(
            {'message': 'date is required in the query param'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if re.search(r'(^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$)', date) is None:
        return Response(
            {'message': 'date is value should be YYYY-MM-DD format'},
            status=status.HTTP_400_BAD_REQUEST
        )

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(owner_id) FROM bookings_booking WHERE departing_date = %s", [date])
        database_result = cursor.fetchall()
    if len(database_result):
        for item in database_result[0]:
            result = item

    return Response({'result': result}, status=status.HTTP_200_OK)
