from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import QuerySet


# Create your models here.
class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateTimeField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+375(24|25|29|33|44)\d{7}$',
        message="Phone number should start with +375 and consist of 13 digits. For exemple +375291231212 "
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True)  # Validators should be a list
    objects: QuerySet

    def __str__(self):
        return f"Profile: {self.user.username}"
