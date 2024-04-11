from django import forms
from . import models
from . import tasks


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
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control magic-mint-focus'}))
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control magic-mint-focus', 'rows': 5, 'placeholder': 'Enter your question here...'}))

    class Meta:
        model = models.Question
        fields = ['name', 'text', 'theme']
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
    #         tasks.create_thumbnail_image.delay(instance.__class__.__name__, instance.id, (100, 100))
    #
    #     return instance
