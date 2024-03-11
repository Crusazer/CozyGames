import django.db.models.signals
from django.contrib.auth.models import User
from django.dispatch import receiver

from users.models import Profile


@receiver(django.db.models.signals.post_save, sender=User)
def create_profile(sender, instance: User, created: bool, **kwargs):
    if created:
        instance.profile = Profile.objects.create(user=instance)
        instance.profile.save()
