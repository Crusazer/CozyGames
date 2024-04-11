from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.core import validators

from cozygames_core import settings


class Theme(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    date_created = models.DateField(auto_now_add=True, null=False)
    objects: QuerySet

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=300, null=False, blank=False)
    text = models.TextField(max_length=500, null=False, blank=True, default='')
    theme = models.ForeignKey(Theme, related_name='questions', null=False, blank=False, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='questions', null=False, blank=False, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, null=False)
    date_update = models.DateField(auto_now=True, null=False)
    objects: QuerySet

    def __str__(self):
        return self.title


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


class ClientReview(models.Model):
    user = models.ForeignKey(User, related_name='user', null=True, blank=True, on_delete=models.SET_NULL)
    text = models.TextField(blank=False, null=False)
    rating = models.PositiveSmallIntegerField(blank=False, null=False, validators=[validators.MinValueValidator(0),
                                                                                   validators.MaxValueValidator(5)])
    date_posted = models.DateTimeField(auto_now_add=True, null=False)
    image = models.ImageField(upload_to='client_reviews/', blank=True, null=True)
    objects: QuerySet

    def get_photo_url(self) -> str | None:
        if self.image:
            return self.image.url

    def get_thumbnail_url(self) -> str | None:
        if self.image:
            thumbnail_name = 'thumbnails/' + self.image.name.split('/')[-1]
            return settings.MEDIA_URL + thumbnail_name
        return None

    def __str__(self):
        return f"Review from {self.user or 'anonymous'} on {self.date_posted}"


class Article(models.Model):
    title = models.CharField(max_length=300, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    date_posted = models.DateField(auto_now_add=True, null=False)
    objects: QuerySet

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    article = models.ForeignKey(Article, related_name='images', null=False, blank=False, on_delete=models.CASCADE)
    objects: QuerySet

    def __str__(self):
        return f"Image from {self.article.title}"
