from django.test import TestCase
from django.http import HttpRequest, HttpResponseRedirect, Http404, HttpResponse
from buddy import views
from ..common import database_seed
from buddy.models import Course
import codecs


class AddAndEnrollInClasses(TestCase):
    # Populating the database
    def setUp(self):
        database_seed.seed()


    def test_add_subject(self):
        x = 0
        self.client.login(username="Professor-1", password="LxrUJHz9")
        response = self.client.post('/professor/addSubject', {'course_code': ['TDT5085'], 'name': ['Encryption'], 'description': ['This is the encryption subject']})
        if Course.objects.filter(course_code='TDT5085'):
            x = 1
        self.assertEqual(response.status_code, 302)
        self.assertEqual(x, 1)


    def test_student_add_subject(self):
        self.client.login(username="Student-5", password="bUd2kj55")
        response = self.client.post('/professor/addSubject', {'course_code': ['TDT5082'], 'name': ['Encryptions'], 'description': ['Sis is the encryption subject']})
        self.assertEqual(response.status_code, 302)


    def test_student_enroll_in_class(self):
        self.client.login(username="Student-5", password="bUd2kj55")
        courses = views.get_all_courses()
        response = self.client.post('/student/enroll', {'course': courses[0].course_code})
        self.assertEqual(response.status_code, 302)
