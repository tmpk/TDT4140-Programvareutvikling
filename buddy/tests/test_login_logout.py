from django.test import TestCase
from django.http import HttpRequest, HttpResponseRedirect, Http404, HttpResponse
from buddy.view import login_views
from buddy.models import Profile
from ..common import database_seed
import codecs


class LoginAndOut(TestCase):
    # Populating the database
    def setUp(self):
        database_seed.seed()

    def test_login(self):
        response = self.client.post('/index')
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/account/login', {'username': ['Student-1'], 'password': ['psEruWTg']})
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/index')
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.post('/account/login', {'username': ['Professor-1'], 'password': ['LxrUJHz9']})
        self.assertEqual(response.status_code, 302)


    def test_logout(self):
        self.client.login(username="Professor-1", password="LxrUJHz9")
        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 302)
