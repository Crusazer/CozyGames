from django import forms
from django.utils import timezone


class DateInput(forms.DateInput):
    input_type = 'date'


class BookingDateForm(forms.Form):
    """ Booking date form to choice a date in the calendar """

    date = forms.DateField(
        widget=DateInput(attrs={'min': timezone.datetime.today().strftime('%Y-%m-%d'),
                                'max': (timezone.datetime.today() + timezone.timedelta(days=10)).strftime('%Y-%m-%d')}))
