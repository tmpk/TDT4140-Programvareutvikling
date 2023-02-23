from django.test import TestCase, RequestFactory
from buddy.views import *
from ..common import database_seed
from buddy.models import Quiz, Course, CompletedQuestion
from django.contrib.auth.models import User


class GetQuizzesTestCase(TestCase):

    def setUp(self):
        database_seed.seed()
        self.factory = RequestFactory()
        self.client.login(username="Student-1", password="psEruWTg")
        self.user=User.objects.filter(username="Student-1").get()



    def test_get_completed_quizzes(self):
        "only quizzes completed by a given student should be returned"
        course1 = Course.objects.filter(course_code='TDT4120').get()
        quiz1=Quiz.objects.get(name='Comparison sorts')
        quiz2=Quiz.objects.get(name='P vs. NP')
        self.assertQuerysetEqual(get_completed_quizzes(self, course1.course_code), [])
        completedquiz1 = CompletedQuiz(quiz=quiz1, student_id=self.user)
        completedquiz1.save()
        self.assertQuerysetEqual(get_completed_quizzes(self, course1.course_code), ['<Quiz: Comparison sorts>'])
        completedquiz2 = CompletedQuiz(quiz=quiz2, student_id=self.user)
        completedquiz2.save()
        self.assertQuerysetEqual(get_completed_quizzes(self, course1.course_code), ['<Quiz: Comparison sorts>', '<Quiz: P vs. NP>'])