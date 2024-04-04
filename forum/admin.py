from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    pass
