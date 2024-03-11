from django.urls import path
from . import views

app_name = 'cozygames'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('booking/', views.BookingView.as_view(), name='booking'),
]
