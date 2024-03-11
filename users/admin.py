from django.contrib import admin
from django.contrib.auth.models import User

from cozygames.admin import ReservationInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import Profile


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, ReservationInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
