"""
The database models for the program
"""
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# Create your models here.

# Get a reference to the user models
# See http://bit.ly/2lfhkD1 (Stackoverflow)
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Course(models.Model):
    """
    Entity model representing a course

    The course model represents an entity class that students can
    enroll in.
    """
    COURSE_ID = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __str__(self):
        """Returns the course as a string"""
        return self.course_code + " - " + self.name

class Quiz(models.Model):
    """
    Entity model for a quiz
    """
    QUIZ_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    active_from = models.DateTimeField(default='2017-01-01')

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    question belonging to a quiz
    """
    QUESTION_ID = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    multiple_correct_answers = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text


class QuizIsCreatedByTa(models.Model):
    """
    The quiz has been created by a ta
    """
    CREATED_BY_TA_ID = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.quiz)


class QuestionIsEditedByTa(models.Model):
    """
    The quiz has been edited by a ta
    """
    EDITED_BY_TA_ID = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.question)


class Answer(models.Model):
    """
    answer alternative to a question
    """
    ANSWER_ID = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    correct_answer = models.BooleanField()
    answer_count = models.IntegerField(default=0)

    def __str__(self):
        return self.answer_text

    def is_correct(self):
        return self.correct_answer

class Enrollment(models.Model):
    """
    Entity model for a student enrolling in a class

    All student users participation/enrollment in a class will be
    represented by an enrolment entry.
    """
    ENROLLMENT_ID = models.AutoField(primary_key=True)
    student = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        """Returns the relation as a string"""
        return str(self.student) + " - " + str(self.course)


class CourseAdministrator(models.Model):
    """
    Entity model representing an administration relation on a class

    All professors/TA's who will have access to creating or modifying
    a quiz or viewing the result of a quiz will need to be registered
    as a course administrator.
    """
    COURSEADMINISTRATOR_ID = models.AutoField(primary_key=True)
    administrator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        """Returns the relation as a string"""
        return str(self.administrator) + " - " + str(self.course)

class Profile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_professor = models.BooleanField(default=False)

class CompletedQuiz(models.Model):
    """
    entity model representing the case that a student has completed
    a given quiz
    """
    COMPLETEDQUIZ_ID = models.AutoField(primary_key=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    quiz = models.ForeignKey(Quiz)
    student_id = models.ForeignKey(AUTH_USER_MODEL)

class CompletedQuestion(models.Model):
    """
    entity model representing the answer a student has given to a Question
    """
    COMPLETEDQUESTION_ID=models.AutoField(primary_key=True)
    completed_quiz=models.ForeignKey(CompletedQuiz)
    given_answer=models.ForeignKey(Answer)
    cq_text = models.CharField(max_length=200)
    mca = models.BooleanField(default=False)
    correct_a=models.BooleanField(default=False)
    q_id=models.ForeignKey(Question)

    def __str__(self):
        return self.cq_text


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
