from django.test import TestCase
from django.http import HttpRequest, HttpResponseRedirect, Http404, HttpResponse
from buddy.view import professor_views, quiz_views, question_views, answer_views
from buddy.models import QuizIsCreatedByTa, Quiz, Question, QuestionIsEditedByTa
from ..common import database_seed
import codecs


class AddQuizChangesTestCase(TestCase):
    def setUp(self):
        database_seed.seed()

    # Student-1 add a quizself.
    def test_ta_create_quiz(self):
        self.client.login(username="Student-1", password="psEruWTg")
        response = self.client.post('/quiz/1/add', {'active_from': ['2017-01-01'], 'name': ['new quiz'], 'due_date': ['2017-06-08']})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/quiz/2/add', {'active_from': ['2017-01-01'], 'name': ['new Quiz'], 'due_date': ['2017-06-08']})
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        quiz = Quiz.objects.filter(name='new quiz')
        self.client.login(username="Professor-1", password="LxrUJHz9")
        response = self.client.post('/quiz/4/edit', {'quiz_id': ['4']})
        response = self.client.post('/quiz/4/edit', {'quiz_id': ['4']})
        if not QuizIsCreatedByTa.objects.filter(quiz=quiz):
            self.assertEqual(response.status_code, 200)

    # Student-5 tries to add quiz. Should fail.
    def test_not_ta_create_quiz(self):
        self.client.login(username="Student-5", password="bUd2kj55")
        response = self.client.post('/quiz/1/add')
        self.assertEqual(response.status_code, 200)

    # Student-1 tries to add a question.
    def test_ta_create_question(self):
        self.client.login(username="Student-1", password="psEruWTg")
        response = self.client.post('/question/add/1', {'question_text': ['question1']})
        self.assertEqual(response.status_code, 302)
        self.client.post('/logout')
        question = Question.objects.filter(QUESTION_ID='1')
        self.client.login(username="Professor-1", password="LxrUJHz9")
        response = self.client.post('/question/1/edit', {'question_text': ['question1']})
        if not QuestionIsEditedByTa.objects.filter(question=question):
            self.assertEqual(response.status_code, 200)


    # Student-5 tries to add a question.
    def test_not_ta_create_question(self):
        self.client.login(username="Student-5", password="bUd2kj55")
        response = self.client.post('/question/add/1')
        self.assertEqual(response.status_code, 302)

    # Student-1 tries to change a question.
    def test_ta_change_question(self):
        self.client.login(username="Student-1", password="psEruWTg")
        response = self.client.post('/question/1/edit', {'question_text': ['question1 to 2']})
        self.assertEqual(response.status_code, 200)

    # Student-5 tries to add a question.
    def test_not_ta_change_question(self):
        self.client.login(username="Student-5", password="bUd2kj55")
        response = self.client.post('/question/1/edit', {'question_text': ['question1 to 2']})
        self.assertEqual(response.status_code, 302)
