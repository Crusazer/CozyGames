from django.contrib import admin
from . import models


# Register your models here.
class MessagesInline(admin.TabularInline):
    model = models.Message
    verbose_name_plural = 'messages'
    extra = 0


class ArticleImagesInline(admin.TabularInline):
    model = models.ArticleImage
    verbose_name_plural = 'Images'
    extra = 0


class TournamentParticipantsInline(admin.TabularInline):
    model = models.TournamentParticipant
    verbose_name_plural = 'Tournament participants'
    extra = 0


class TournamentWinnersInline(admin.TabularInline):
    model = models.TournamentWinner
    verbose_name_plural = 'Winners'
    extra = 0


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (MessagesInline,)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ClientReview)
class ClientReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = (ArticleImagesInline,)


@admin.register(models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    inlines = (TournamentParticipantsInline, TournamentWinnersInline)


@admin.register(models.TournamentParticipant)
class TournamentParticipant(admin.ModelAdmin):
    pass
