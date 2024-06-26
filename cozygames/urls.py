from django.urls import path
from django.views.i18n import JavaScriptCatalog

from . import views

app_name = 'cozygames'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('booking_table/', views.BookingTableView.as_view(), name='booking_table'),
    path('booking/cancel_bookings/', views.CancelReservation.as_view(), name='cancel_bookings'),
    path('booking/booking_history/', views.BookingHistoryView.as_view(), name='booking_history'),
    path('booking/voting/', views.VotingView.as_view(), name='voting'),
    path('booking/card_game_info/<int:game_id>/', views.CardGameInfoView.as_view(), name='card_game_info'),
]
