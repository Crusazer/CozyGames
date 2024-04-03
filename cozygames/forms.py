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
    """Form for voting for a game."""
    game_choices = [(game.id, game.name) for game in CardGame.objects.all()]
    game = forms.ChoiceField(choices=game_choices, label='Select a game')
