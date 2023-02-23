from django.test import TestCase, RequestFactory
from buddy.views import *
from ..common import database_seed
from buddy.models import Quiz, Course, CompletedQuestion
from django.contrib.auth.models import User


class GetCompletedQuizzesTestCase(TestCase):

    def setUp(self):
        database_seed.seed()
        self.factory = RequestFactory()
        self.client.login(username="Student-1", password="psEruWTg")
        self.user=User.objects.filter(username="Student-1").get()


    def test_upcoming_quizzes(self):
        
        """
        only quizzes that are not completed and with a future due date should be returned 
        as an upcoming quiz. 
        """
        course1 = Course.objects.filter(course_code='TDT4120').get()
        quiz1=Quiz.objects.get(name='Comparison sorts')
        quiz2=Quiz.objects.get(name='P vs. NP')
        quiz1.due_date='2020-01-01'
        quiz1.save()
        quiz2.due_date='2020-01-01'
        quiz2.save()
        self.assertQuerysetEqual(get_upcoming_quizzes(self, course1.course_code), ['<Quiz: Comparison sorts>', '<Quiz: P vs. NP>'])
        completedquiz1 = CompletedQuiz(quiz=quiz1, student_id=self.user)
        completedquiz1.save()
        self.assertQuerysetEqual(get_upcoming_quizzes(self, course1.course_code), ['<Quiz: P vs. NP>'])
        quiz2.due_date='2010-01-01'
        quiz2.save()
        self.assertQuerysetEqual(get_upcoming_quizzes(self, course1.course_code), [])
        
        