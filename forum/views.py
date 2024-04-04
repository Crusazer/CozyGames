from django.shortcuts import render
from django.urls import reverse
from django.views import generic, View
from . import models


class ThemesView(generic.ListView):
    model = models.Theme
    template_name = 'forum/themes.html'
    context_object_name = 'themes'
