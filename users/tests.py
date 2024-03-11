from http.client import HTTPResponse

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .forms import CreateUserForm, LoginUserForm


# Create your tests here.
class RegistrationTest(TestCase):
    user_data = {
        'username': 'testuser',
        'email': 'testemail@email.com',
        'password1': 'test1234',
        'password2': 'test1234'
    }
    url = reverse('user:registration')

    def test_register_user_view(self):
        response = self.client.post(self.url, data=self.user_data)

        self.assertTrue(response.status_code, 200)
        user: User = get_user_model().objects.filter(username=self.user_data['username']).first()
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])

    def test_register_user_form_valid_data(self):
        form = CreateUserForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_register_user_form_invalid_data(self):
        form = CreateUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # Username, email and password (1 and 2) fields are void

    def test_register_user_form_save(self):
        form = CreateUserForm(data=self.user_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, get_user_model())
        self.assertEqual(user.username, self.user_data['username'])


class LoginUserTest(TestCase):
    url = reverse('user:login')

    @classmethod
    def setUpTestData(cls):
        cls.user: User = get_user_model().objects.create_user(username='testuser', password='test1234')

    def test_login_user_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_login_user_form_valid_data(self):
        form = LoginUserForm(data={'username': 'testuser', 'password': 'test1234'})
        self.assertTrue(form.is_valid())

    def test_login_user_form_invalid_data(self):
        form = LoginUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Assuming both username and password are required fields

    def test_login_user(self):
        response = self.client.post(self.url, data={'username': 'testuser', 'password': 'test1234'})
        self.assertRedirects(response, '/')

    def test_login_user_with_invalid_credentials(self):
        response = self.client.post(self.url, data={'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)

