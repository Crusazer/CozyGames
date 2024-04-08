from django import forms
from . import models


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
