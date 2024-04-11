from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Table(models.Model):
    class Type(models.TextChoices):
        BOARD = "BG", _("board game")
        CONSOLE = "CG", _("console game")

    number: int = models.IntegerField(unique=True, blank=False, null=False, default=0)
    type: str = models.CharField(max_length=2, choices=Type, default=Type.BOARD)
    objects: QuerySet

    def __str__(self):
        return f"Table #{self.number}  {self.get_type_display()}"


class Reservation(models.Model):
    user: User = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    table: Table = models.ForeignKey(Table, related_name='reservations', on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    objects: QuerySet

    def __str__(self):
        return f"Reservation of table #{self.table.number} on {self.date}"


class CardGame(models.Model):
    name = models.CharField(max_length=100, null=False)
    min_number_player = models.PositiveIntegerField(null=False, blank=False)
    max_number_player = models.PositiveIntegerField(null=False, blank=False)
    description = models.TextField(null=True, blank=True, default='No description.')
    objects: QuerySet

    def __str__(self):
        return f"{self.name}"


class Voting(models.Model):
    date = models.DateField(null=False, unique_for_date=True, auto_now=False, auto_now_add=True)
    result = models.ForeignKey(CardGame, related_name='votings', blank=True, null=True, default=None,
                               on_delete=models.SET_NULL)
    objects: QuerySet

    def __str__(self):
        return f"Voting of {self.date}"


class Vote(models.Model):
    user = models.ForeignKey(User, related_name='votes', null=True, blank=False, on_delete=models.SET_NULL)
    card_game = models.ForeignKey(CardGame, related_name='votes', null=False, blank=False, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, related_name='votes', blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    objects: QuerySet

    def __str__(self):
        return f"Vote of {self.user} for {self.card_game.name} on {self.date}"

    class Meta:
        unique_together = ('user', 'date', 'card_game')

    @classmethod
    def user_can_vote(cls, user: User, date) -> bool:
        """Checks if the user can vote on the given date."""
        return cls.objects.filter(user=user, date=date).count() < 3
