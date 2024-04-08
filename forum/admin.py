from django.contrib import admin
from . import models


# Register your models here.
class MessagesInline(admin.TabularInline):
    model = models.Message
    verbose_name_plural = 'messages'
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
