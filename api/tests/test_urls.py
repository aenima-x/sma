from django.test import SimpleTestCase
from django.urls import resolve, reverse

from api.views import signup_view, get_stocks_view


class TestUrls(SimpleTestCase):

    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup_view)

    def test_get_stocks_url_is_resolver(self):
        url = reverse('get_stocks', kwargs={'symbol': 'AAPL'})
        self.assertEquals(resolve(url).func, get_stocks_view)
