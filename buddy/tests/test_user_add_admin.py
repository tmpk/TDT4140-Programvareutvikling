from django.test import TestCase
from django.http import HttpRequest, HttpResponseRedirect, Http404, HttpResponse
from buddy.view import professor_views
from ..common import database_seed
import codecs


class AddTaTestCase(TestCase):
    def setUp(self):
        database_seed.seed()

    # Professor, admin for this course adds a user.
    def test_add_ta(self):
        self.client.login(username="Professor-1", password="LxrUJHz9")
        response = self.client.post('/add_ta/TDT4120', {'student_email': ['user2@stud.ntnu.no']})
        #add_student_assistant(response, 'TDT4120')
        self.assertEqual(response.status_code, 302)

    # Professor, not admin for this course adds user.
    def test_add_ta_as_not_prof_admin(self):
        self.client.login(username="Professor-2", password="WKQWSaFN")
        response = self.client.post('/add_ta/TDT4120', {'student_email': ['user1@stud.ntnu.no']})
        #add_student_assistant(response, 'TDT4120')
        self.assertEqual(response.status_code, 200)

    # Student tries to add user.
    def test_add_ta_as_student(self):
        self.client.login(username="Student-5", password="bUd2kj55")
        response = self.client.post('/add_ta/TDT4120', {'student_email': ['user2@stud.ntnu.no']})
        #add_student_assistant(response, 'TDT4120')
        self.assertEqual(response.status_code, 200)

    # Student tries to add user.
    def test_add_ta_as_student_and_admin(self):
        self.client.login(username="Student-1", password="psEruWTg")
        response = self.client.post('/add_ta/TDT4120', {'student_email': ['user2@stud.ntnu.no']})
        #add_student_assistant(response, 'TDT4120')
        self.assertEqual(response.status_code, 200)
