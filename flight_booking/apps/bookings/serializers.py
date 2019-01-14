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

    def validate(self, data):
        """
        Validates data
        :param data: contains flight booking data
        :return: data
        """
        flight_type = str(data.get('flight_type'))
        returning_date = data.get('returning_date')

        if flight_type.upper() == 'ROUND' and returning_date is None:
            raise serializers.ValidationError('returning_date is required.')
        if flight_type.upper() == 'ONE' and returning_date:
            data['returning_date'] = None
        return data

    @staticmethod
    def validate_flight_type(flight_type):
        """
        Validates flight_type
        :param flight_type: contains flight_type value
        :return: flight_type
        """
        flight_type = str(flight_type).upper()
        if flight_type not in ('ONE', 'ROUND'):
            raise serializers.ValidationError('flight_type can only be ONE or ROUND.')
        return flight_type


class BookingUpdateSerializer(BookingSerializer):
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
        fields = ('id', 'flight_from', 'flight_to', 'departing_date', 'returning_date', 'flight_type',)