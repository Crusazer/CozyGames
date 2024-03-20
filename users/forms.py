from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.models import Profile


class ReceiverForm(forms.ModelForm):
    phone_number = forms.RegexField(regex=r'^\+375(24|25|29|33|44)\d{7}$', error_messages={
        'invalid': "Phone number should start with +375 and consist of 13 digits. For exemple +375291231212 ", })


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }

    def clean_email(self):
        """ Duplicate email verification or field is empty"""
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("This field is required.")
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class LoginUserForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class': 'form-control'}),
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': "First name",
            'last_name': "Last name",
            'username': "Username",
            'email': "Email"
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birthday', 'phone_number']
        labels = {
            'birthday': "Birthday",
            'phone_number': "Phone Number"
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'class': 'form-input', 'type': 'date', 'max': timezone.now().date()}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'})
        }
