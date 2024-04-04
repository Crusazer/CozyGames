from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.cache import cache_page
from django.utils import timezone

from cozygames.forms import BookingDateForm, VotingForm
from cozygames.models import Table, Reservation, Vote, Voting, CardGame


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
    form_class = BookingDateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        form = BookingDateForm(self.request.POST)
        context = {'form': form}
        if form.is_valid():
            date = form.cleaned_data['date']
            tables = Table.objects.filter(~Q(reservations__date=date))
            context['tables'] = tables
            context['date'] = date
        return render(self.request, 'cozygames/booking.html', context=context)


class BookingTableView(LoginRequiredMixin, View):
    model = Table

    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
        except TypeError:
            messages.warning(request, f'Somthing wrong with data')
            return redirect(reverse('cozygames:booking'))
        days_delta = (date.date() - timezone.now().date()).days

        if days_delta > 10 or days_delta < 0:
            messages.warning(request, f"You cannot book earlier than today or more than 10 days in advance.")

        elif request.user.reservations.filter(date=date):
            messages.warning(request, "You already have reservation that day.")

        elif request.user.reservations.filter(date__gte=timezone.now().date()).count() > 2:
            messages.warning(request, "You cannot have more than 3 reservations at the same time.")

        else:
            table = get_object_or_404(self.model, id=request.POST['table_id'])
            Reservation.objects.create(user=request.user, date=date, table=table)
            messages.success(request, "The table has been successfully booked.")

        return redirect(reverse('cozygames:booking'))


class CancelReservation(LoginRequiredMixin, generic.list.MultipleObjectMixin, generic.View):
    model = Reservation
    context_object_name = 'reservations'
    template_name = 'cozygames/cancel_bookings.html'
    success_url = reverse_lazy('cozygames:cancel_bookings')

    def get_queryset(self):
        return self.request.user.reservations.filter(date__gte=timezone.now().date()).order_by(
            'date').select_related(
            'table')

    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(object_list=self.get_queryset()))

    def post(self, request: HttpRequest, *args, **kwargs):
        reservation = request.user.reservations.filter(id=request.POST.get('reservation_id')).first()
        if reservation:
            reservation_date = reservation.date
            reservation.delete()
            messages.success(request, f"Your booking of {reservation_date} has been successfully canceled.")
        else:
            messages.warning(request, "Booking not found.")
        return redirect(self.success_url)


class BookingHistoryView(LoginRequiredMixin, generic.ListView):
    model = Reservation
    context_object_name = 'reservations'
    template_name = 'cozygames/booking_history.html'
    paginate_by = 12

    def get_queryset(self):
        return self.request.user.reservations.filter(date__lte=timezone.now().date()).order_by('-date')


class VotingView(generic.View):
    template_name = 'cozygames/voting.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        left_votes = 0
        if self.request.user.is_authenticated:
            left_votes = 3 - Vote.objects.filter(user=self.request.user, date=timezone.now().date()).count()

        context = {
            'form': VotingForm(),
            'left_votes': left_votes
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request: HttpRequest, *args, **kwargs):
        # schedule_tasks.update_voting.delay()
        form = VotingForm(request.POST)
        if form.is_valid():
            today_date = timezone.now().date()
            voting = get_object_or_404(Voting, date=today_date)
            card_game = get_object_or_404(CardGame, pk=form.cleaned_data['game'])
            if Vote.objects.filter(user=self.request.user, date=today_date).count() >= 3:
                messages.warning(request, "You cannot vote more than 3 times.")
            else:
                try:
                    Vote.objects.create(user=request.user, card_game=card_game, voting=voting)
                    messages.success(request, "Your vote has been recorded successfully.")
                except IntegrityError:
                    messages.warning(request, "You have already voted for this game.")

        return redirect(reverse_lazy('cozygames:voting'))


class CardGameInfoView(View):
    def get(self, request, game_id):
        game = get_object_or_404(CardGame, pk=game_id)
        return render(request, 'cozygames/card_game_info.html', {'game': game})

    def post(self, request, game_id):
        return HttpResponseBadRequest("Invalid request")
