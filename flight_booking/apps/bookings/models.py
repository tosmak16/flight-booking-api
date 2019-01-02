from django.db import models
from django.utils import timezone
from datetime import date

from ..users.models import User


class Booking(models.Model):

    """Flight booking model"""

    # One represents one-way trip while round represents round-way trip
    BOOKING_TYPE = (('ONE', 'O'), ('ROUND', 'R'))

    flight_from = models.CharField(max_length=100)
    flight_to = models.CharField(max_length=100)
    departing_date = models.DateField(default=date.today)
    returning_date = models.DateField(blank=True, null=True)
    flight_type = models.CharField(max_length=10, choices=BOOKING_TYPE, default='ONE')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester')

    def __str__(self):
        return f'{self.owner}, {self.flight_from}, {self.departing_date}'

