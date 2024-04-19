from django import forms
from django.utils import timezone

from . import models
from . import tasks

from django.contrib.admin import widgets
import datetime


class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ['text', 'question']
        widgets = {
            'question': forms.HiddenInput(),
            'text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your message here...'})
        }
        auto_id = False

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text.strip():  # Check if the text contains only spaces or an empty string
            raise forms.ValidationError("Message text cannot be empty.")
        return text


class CreateQuestionForm(forms.ModelForm):
    theme = forms.ModelChoiceField(queryset=models.Theme.objects.all(), label="Select theme",
                                   widget=forms.Select(attrs={'class': 'form-select magic-mint-focus'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control magic-mint-focus'}))
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control magic-mint-focus', 'rows': 5, 'placeholder': 'Enter your question here...'}))

    class Meta:
        model = models.Question
        fields = ['title', 'text', 'theme']
        widgets = {
            'author': forms.HiddenInput(),
        }


class CreateReviewForm(forms.ModelForm):
    class Meta:
        RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
        model = models.ClientReview
        fields = ('text', 'rating', 'image')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control magic-mint-focus', 'rows': 5,
                                          'placeholder': 'Enter your review here...'}),
            'rating': forms.Select(choices=RATING_CHOICES, attrs={'class': 'form-select magic-mint-focus'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control magic-mint-focus'}),
        }

    # def save(self, commit=True, *args, **kwargs):
    #     instance = super().save(*args, **kwargs)
    #     if instance.image and commit:
    #         tasks.create_thumbnail_image.delay(instance.__class__.__name__, instance.id, (75, 75))
    #
    #     return instance


class CreateTournamentForm(forms.ModelForm):
    class Meta:
        model = models.Tournament
        exclude = ('approved',)

        widgets = {
            'author': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control magic-mint-focus'}),
            'prize_pool': forms.TextInput(attrs={'class': 'form-control magic-mint-focus'}),
            'prize_distribution': forms.Textarea(attrs={'class': 'form-control magic-mint-focus', 'rows': 5,
                                                        'placeholder': 'Enter prize distribution...'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control magic-mint-focus', 'type': 'datetime-local'}),
            'max_players': forms.NumberInput(attrs={'class': 'form-control magic-mint-focus'}),
            'rules': forms.Textarea(attrs={'class': 'form-control magic-mint-focus', 'rows': 5,
                                           'placeholder': 'Enter tournament rules...'}),
            'type': forms.Select(attrs={'class': 'form-select magic-mint-focus'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now() + timezone.timedelta(days=3):
            raise forms.ValidationError("The tournament cannot start earlier than 3 days from now.")

        if date.time() < datetime.time(10, 0) or date.time() > datetime.time(18, 0):
            raise forms.ValidationError("The time should be between 10:00 and 18:00.")

        if self.cleaned_data.get('title'):
            raise forms.ValidationError("The title can't be empty.")

        if self.cleaned_data.get('prize_pool'):
            raise forms.ValidationError("The prize pool can't be empty.")

        return date
