from django import forms
from django.utils import timezone

from cozygames.models import CardGame


class DateInput(forms.DateInput):
    input_type = 'date'


class BookingDateForm(forms.Form):
    """ Booking date form to choice a date in the calendar """

    date = forms.DateField(
        widget=DateInput(attrs={'min': timezone.datetime.today().strftime('%Y-%m-%d'),
                                'max': (timezone.datetime.today() + timezone.timedelta(days=10)).strftime('%Y-%m-%d')}))


class VotingForm(forms.Form):
    """Voting for to vote from game"""
    game_choices = CardGame.objects.all().values_list('id', 'name')
    game = forms.ChoiceField(choices=game_choices, label='Select a game')
