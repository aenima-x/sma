

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TestView(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.valid_user_data = {"email": "user@email.com",
                                "name": "name",
                                "lastname": "lastname"}
        self.invalid_user_data = {"email": "invalidEmail",
                                  "name": "name",
                                  "lastname": "lastname"}
        self.user = User.objects.create_user("someuser@email.com")
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.token.save()

    def test_signup_invalid_email(self):
        response = self.client.post(reverse('signup'), self.invalid_user_data, format='json')
        self.assertEquals(response.status_code, 400)

    def test_signup_valid_email(self):
        response = self.client.post(reverse('signup'), self.valid_user_data, format='json')
        self.assertEquals(response.status_code, 200)

    def test_signup_create_user(self):
        self.assertFalse(User.objects.filter(username=self.valid_user_data['email']).exists())
        response = self.client.post(reverse('signup'), self.valid_user_data, format='json')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=self.valid_user_data['email']).exists())

    def test_get_stocks_token_required(self):
        response = self.client.post(reverse('get_stocks', kwargs={'symbol': 'AAPL'}))
        self.assertEquals(response.status_code, 401)

    def test_get_stocks_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('get_stocks', kwargs={'symbol': 'AAPL'}))
        self.assertEquals(response.status_code, 200)

    def test_get_stocks_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token INVALID_TOKEN')
        response = self.client.post(reverse('get_stocks', kwargs={'symbol': 'AAPL'}))
        self.assertEquals(response.status_code, 401)

