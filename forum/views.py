from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page

from . import forms, tasks, models


class ThemesView(generic.ListView):
    model = models.Theme
    template_name = 'forum/themes.html'
    context_object_name = 'themes'


class QuestionsView(generic.ListView):
    model = models.Question
    template_name = 'forum/questions.html'
    context_object_name = 'questions'

    def get_queryset(self):
        theme_id = self.kwargs.get('theme_id')
        if theme_id:
            return self.model.objects.filter(theme__id=theme_id)
        return [self.model.objects.first()]


class QuestionDetail(generic.DetailView):
    model = models.Question
    template_name = 'forum/question_detail.html'
    context_object_name = 'question'
    pk_url_kwarg = 'question_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_messages'] = context['question'].messages.all()
        context['form'] = forms.MessageForm()
        return context


class CreateMessageView(LoginRequiredMixin, generic.FormView):
    template_name = 'forum/question_detail.html'
    form_class = forms.MessageForm

    def form_valid(self, form):
        message = form.save(commit=False)
        message.question = form.cleaned_data['question']
        message.user = self.request.user
        message.save()
        return redirect(reverse('forum:question_detail', kwargs={'question_id': form.cleaned_data['question'].pk}))

    def form_invalid(self, form):
        messages.warning(self.request, "You are trying to send the wrong message.")
        return super().form_invalid(form)


class CreateQuestionView(LoginRequiredMixin, generic.FormView):
    template_name = 'forum/create_question.html'
    form_class = forms.CreateQuestionForm

    def form_valid(self, form: forms.forms.ModelForm):
        question = form.save(commit=False)
        question.author = self.request.user
        question.theme = form.cleaned_data['theme']
        question.save()
        return redirect(reverse('forum:questions', kwargs={'theme_id': form.cleaned_data['theme'].id}))

    def form_invalid(self, form):
        messages.warning(self.request, "Incorrect input.")
        return super().form_invalid(form)


class ClientReviewView(generic.ListView):
    model = models.ClientReview
    ordering = ('-date_posted',)
    context_object_name = 'client_reviews'
    template_name = 'forum/client_reviews.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = forms.CreateReviewForm()
        return context


class CreateClientReviewView(generic.FormView):
    template_name = 'forum/client_reviews.html'
    form_class = forms.CreateReviewForm

    def form_valid(self, form: forms.CreateReviewForm):
        review = form.save(commit=False)
        if self.request.user.is_authenticated:
            review.user = self.request.user
        else:
            review.user = None
        review.save()
        tasks.create_thumbnail_image.delay(review.__class__.__name__, review.id, (75, 75))
        return redirect(reverse('forum:client_reviews'))


class BlogView(generic.ListView):
    model = models.Article
    ordering = ('-date_posted', '-pk')
    context_object_name = 'articles'
    template_name = 'forum/articles.html'
    paginate_by = 10
    queryset = model.objects.all().prefetch_related('images')


class TournamentsView(generic.ListView):
    model = models.Tournament
    ordering = ('-date', '-pk')
    context_object_name = 'tournaments'
    template_name = 'forum/tournaments.html'

    def get_queryset(self):
        return self.model.objects.filter(date__gte=timezone.now(), approved=True).all()


class FinishedTournamentsView(generic.ListView):
    model = models.Tournament
    ordering = ('-date', '-pk')
    context_object_name = 'tournaments'
    template_name = 'forum/finished_tournaments.html'

    @classmethod
    def as_view(cls):
        view = super().as_view()
        return cache_page(60 * 60 * 1)(view)  # Cache the page for 3 hours

    def get_queryset(self):
        return self.model.objects.filter(date__lte=timezone.now(), approved=True).all()


class TournamentDetailView(generic.DetailView):
    model = models.Tournament
    template_name = 'forum/tournament_detail.html'
    context_object_name = 'tournament'
    pk_url_kwarg = 'tournament_id'

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch('participants', queryset=models.TournamentParticipant.objects.select_related('user'))
        )


class FinishedTournamentDetailView(generic.DetailView):
    model = models.Tournament
    template_name = 'forum/finished_tournament_detail.html'
    context_object_name = 'tournament'
    pk_url_kwarg = 'tournament_id'

    @classmethod
    def as_view(cls):
        view = super().as_view()
        return cache_page(60 * 60 * 3)(view)  # Cache the page for 3 hours

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch('winners', queryset=models.TournamentWinner.objects.select_related('user')),
            Prefetch('participants', queryset=models.TournamentParticipant.objects.select_related('user'))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if models.TournamentParticipant.objects.filter(tournament=self.kwargs.get('tournament_id'),
                                                           user=self.request.user).first():
                context['user_is_joined'] = True
        return context

    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        tournament: models.Tournament = self.model.objects.filter(pk=self.request.POST.get('tournament_id', 0)).first()

        if not tournament:
            messages.warning(self.request, 'This tournament non exists')

        elif timezone.now() > tournament.date:
            messages.warning(self.request, "You can't join to finished the tournament.")

        elif models.TournamentParticipant.objects.filter(user=self.request.user, tournament=tournament):
            messages.warning(self.request, "You have already submitted")

        else:
            tournament_participant = models.TournamentParticipant(user=self.request.user, tournament=tournament)
            if tournament.type == models.Tournament.Type.OPEN:
                tournament_participant.status = models.TournamentParticipant.Status.APPROVED
                messages.success(self.request, "You have joined the tournament.")
            else:
                messages.success(self.request, "Your application has been accepted.")
            tournament_participant.save()

        return redirect(
            reverse('forum:tournament_detail', args=(tournament.pk,))) if tournament else (
            redirect('forum:tournaments'))


class AddParticipantView(LoginRequiredMixin, generic.View):
    model = models.Tournament

    def post(self, *args, **kwargs):
        tournament = get_object_or_404(self.model, pk=self.request.POST.get('tournament_id', 0))

        if self.request.user == tournament.author:
            participant: models.TournamentParticipant = get_object_or_404(models.TournamentParticipant,
                                                                          pk=self.request.POST.get('participant_id', 0))
            if tournament.participants.count() < tournament.max_players:
                participant.status = models.TournamentParticipant.Status.APPROVED
                participant.save()
                messages.success(self.request, f"{participant.user.username} has been successfully added to "
                                               f"the list of participants.")
            else:
                messages.warning(self.request,
                                 f"{participant.user.username} was not added. Maximum number of players reached"
                                 f" in the tournament.")

        return redirect(reverse('forum:tournament_detail', args=(tournament.pk,)))


class RemoveParticipantView(LoginRequiredMixin, generic.View):
    model = models.Tournament

    def post(self, *args, **kwargs):
        tournament = get_object_or_404(self.model, pk=self.request.POST.get('tournament_id', 0))

        if self.request.user == tournament.author:
            participant: models.TournamentParticipant = get_object_or_404(models.TournamentParticipant,
                                                                          pk=self.request.POST.get('participant_id', 0))

            if tournament.type == self.model.Type.OPEN:
                participant.delete()
            elif tournament.type == models.Tournament.Type.CLOSED:
                participant.status = models.TournamentParticipant.Status.PENDING
                participant.save()

            messages.success(self.request,
                             f"{participant.user.username} has been successfully excluded from the list of "
                             f"participants.")

        return redirect(reverse('forum:tournament_detail', args=(tournament.pk,)))


class LeaveTournamentView(LoginRequiredMixin, generic.View):
    def post(self, *args, **kwargs):
        tournament = get_object_or_404(models.Tournament, pk=self.request.POST.get('tournament_id', 0))
        participant = models.TournamentParticipant.objects.filter(user=self.request.user, tournament=tournament).first()
        if participant:
            participant.delete()
            messages.success(self.request, "You have left the tournament.")
        return redirect(reverse('forum:tournament_detail', args=(tournament.pk,)))


class CreateTournamentView(LoginRequiredMixin, generic.FormView):
    template_name = 'forum/create_tournament.html'
    form_class = forms.CreateTournamentForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "The tournament has been successfully created. Please await moderator "
                                       "approval.")
        return redirect(reverse('forum:tournaments'))
