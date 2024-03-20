import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.forms import SelectDateWidget
from django.utils import timezone
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
