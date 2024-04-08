from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet


class Theme(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    date_created = models.DateField(auto_now_add=True, null=False)
    objects: QuerySet

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    text = models.TextField(max_length=500, null=False, blank=True, default='')
    theme = models.ForeignKey(Theme, related_name='questions', null=False, blank=False, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='questions', null=False, blank=False, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, null=False)
    date_update = models.DateField(auto_now=True, null=False)
    objects: QuerySet

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages", null=False, blank=False, on_delete=models.CASCADE,
                             db_index=True)
    question = models.ForeignKey(Question, related_name="messages", null=False, blank=False, on_delete=models.CASCADE,
                                 db_index=True)
    text = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    objects: QuerySet

    def __str__(self):
        return f"Message from {self.user.username} on {self.date}"
