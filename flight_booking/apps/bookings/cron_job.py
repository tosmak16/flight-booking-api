from datetime import date, timedelta
from django.core.mail import EmailMessage

from .models import Booking
from flight_booking.config.settings import DEFAULT_FROM_EMAIL


def send_flight_reminder_mail():
    tomorrow = date.today() + timedelta(days=1)
    bookings = Booking.objects.filter(departing_date=tomorrow)
    mass_email_list = []
    if not len(bookings):
        return bookings
    for booking in bookings:
        mass_email_list += [booking.owner.email]
    messenger = EmailMessage(
        f"Flight reminder",
        'Hello, this is a reminder that your flight is scheduled for ' + str(tomorrow),
        DEFAULT_FROM_EMAIL,
        to=mass_email_list)
    messenger.send()
