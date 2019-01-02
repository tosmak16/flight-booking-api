from rest_framework import viewsets, mixins

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



