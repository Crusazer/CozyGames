from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('themes/', views.ThemesView.as_view(), name='themes'),
]
