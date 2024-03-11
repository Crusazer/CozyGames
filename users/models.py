from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import QuerySet


# Create your models here.
class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateTimeField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Validators should be a list
    objects: QuerySet

    def __str__(self):
        return f"Profile: {self.user.username}"
