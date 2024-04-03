from django.contrib import admin
from cozygames.models import Reservation, Table, Vote, Voting, CardGame


# Register your models here.
class ReservationInline(admin.TabularInline):
    model = Reservation
    verbose_name_plural = "reservation"
    extra = 0


class VotesInline(admin.TabularInline):
    model = Vote
    verbose_name_plural = 'votes'
    extra = 0


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    inlines = [VotesInline]


@admin.register(CardGame)
class CardGameAdmin(admin.ModelAdmin):
    pass
