from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from . import forms
from . import models


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
