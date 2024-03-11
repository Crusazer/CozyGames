from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page

from cozygames.forms import BookingDateForm
from cozygames.models import Table


# Create your views here.
class IndexView(generic.TemplateView):
    """ This is main page of the site """
    template_name = "cozygames/index.html"

    @method_decorator(cache_page(60 * 15))
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)


class BookingView(generic.TemplateView):
    """ This page for booking tables """
    template_name = 'cozygames/booking.html'

    def get(self, *args, **kwargs):
        kwargs['form'] = BookingDateForm()
        return super().get(self, *args, **kwargs)

    def post(self, *args, **kwargs):
        form = BookingDateForm(self.request.POST)
        context = {'form': form}
        if form.is_valid():
            date = form.cleaned_data['date']
            tables = Table.objects.filter(~Q(reservation__date=date))
            context["tables"] = tables
        return render(self.request, 'cozygames/booking.html', context=context)
