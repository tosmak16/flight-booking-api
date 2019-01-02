from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """
    BookingSerializer
    """
    departing_date = serializers.DateField(
        required=True,
        allow_null=False
    ),

    flight_type = serializers.CharField(
        required=True,
    )

    class Meta:
        model = Booking
        fields = ('id', 'flight_from', 'flight_to', 'departing_date', 'returning_date', 'flight_type', 'owner')






