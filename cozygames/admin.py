from django.contrib import admin
from cozygames.models import Reservation, Table


# Register your models here.
class ReservationInline(admin.TabularInline):
    model = Reservation
    verbose_name_plural = "reservation"
    extra = 0


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    pass
