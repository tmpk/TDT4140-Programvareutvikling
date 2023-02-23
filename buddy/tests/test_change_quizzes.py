from django.test import TestCase
from django.http import HttpRequest, HttpResponseRedirect, Http404, HttpResponse
from buddy.view import professor_views
from ..common import database_seed
import codecs


class ChangeQuizTestCase(TestCase):
    # Populating the database
    def setUp(self):
        database_seed.seed()

        # Tests for creating a quiz
    def test_only_admin_can_create(self):
        self.client.login(username="Professor-1", password="LxrUJHz9")
        self.client.post('/add_ta/TDT4120', {'student_email': ['user1@stud.ntnu.no']})
        response = self.client.post('/quiz/1/add', {'active_from': ['2017-01-01'], 'name': ['new quiz'], 'due_date': ['2017-06-08']})
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        self.client.login(username="Student-1", password="psEruWTg")
        response = self.client.post('/quiz/2/add', {'active_from': ['2017-01-01'], 'name': ['new quiz2'], 'due_date': ['2017-06-09']})
        self.assertEqual(response.status_code, 302)

    def test_others_can_not_create(self):
        self.client.login(username="Professor-2", password="WKQWSaFN")
        response = self.client.post('/quiz/3/add', {'active_from': ['2017-01-01'], 'name': ['new quiz3'], 'due_date': ['2017-07-08']})
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.login(username="Student-5", password="bUd2kj55")
        response = self.client.post('/quiz/4/add', {'active_from': ['2017-01-01'], 'name': ['new quiz4'], 'due_date': ['2017-06-10']})
        self.assertEqual(response.status_code, 200)


        # Tests for editing quiz
    def test_only_admin_can_edit(self):
        self.client.login(username="Professor-1", password="LxrUJHz9")
        self.client.post('/add_ta/TDT4120', {'student_email': ['user1@stud.ntnu.no']})
        response = self.client.post('/quiz/1/edit', {'active_from': ['2017-01-01'], 'name': ['new quizz'], 'due_date': ['2017-06-08']})
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/question/3/add', {'question_text': ['new question3']})
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.login(username="Student-1", password="psEruWTg")
        response = self.client.post('/quiz/1/edit', {'active_from': ['2017-01-01'], 'name': ['new quizzz'], 'due_date': ['2017-06-08']})
        self.assertEqual(response.status_code, 302)

    def test_others_can_not_edit(self):
        self.client.login(username="Professor-2", password="WKQWSaFN")
        response = self.client.post('/quiz/1/edit', {'active_from': ['2017-01-01'], 'name': ['new quizx'], 'due_date': ['2017-06-08']})
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.login(username="Student-5", password="bUd2kj55")
        response = self.client.post('/quiz/1/edit', {'active_from': ['2017-01-01'], 'name': ['new quizzx'], 'due_date': ['2017-06-08']})
        self.assertEqual(response.status_code, 200)


        # Tests for deleting quiz
    def test_only_admin_can_delete(self):
        self.client.login(username="Professor-1", password="LxrUJHz9")
        self.client.post('/add_ta/TDT4120', {'student_email': ['user1@stud.ntnu.no']})
        response = self.client.post('/quiz/3/delete', {'quiz_id': '3'})
        self.client.get('/quiz/3/delete', {'quiz_id': '3'})
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/question/2/delete', {'question_id': ['2']})
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        self.client.login(username="Student-1", password="psEruWTg")
        response = self.client.post('/quiz/3/delete', {'quiz_id': '3'})
        self.assertEqual(response.status_code, 404)

    def test_others_can_not_delete(self):
        self.client.login(username="Professor-2", password="WKQWSaFN")
        response = self.client.post('/quiz/3/delete', {'quiz_id': '3'})
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.login(username="Student-5", password="bUd2kj55")
        response = self.client.post('/quiz/3/delete', {'quiz_id': '3'})
        self.assertEqual(response.status_code, 200)

        # Tests for adding answers
    def test_only_admin_can_add_answer(self):
        self.client.login(username="Professor-1", password="LxrUJHz9")
        response = self.client.post('/answer/1/add', {'answer_text': ['two instances']})

        response = self.client.post('/answer/1/edit', {'answer_text': ['two small instances']})
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        self.client.login(username="Student-1", password="psEruWTg")
        response = self.client.post('/answer/1/edit', {'answer_text': ['twoo small instances']})
        self.assertEqual(response.status_code, 302)
