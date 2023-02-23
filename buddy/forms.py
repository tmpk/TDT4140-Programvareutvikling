from django.forms import ModelForm
from .models import Course, Enrollment, Question, Quiz, Answer, CourseAdministrator


class CourseForm(ModelForm):
    """
    Modelform for courses

    Form representing a course. Chould be used for validation
    before adding or changing data on a course.
    """
    class Meta:
        model = Course
        fields = ['course_code', 'name', 'description']


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'due_date', 'active_from']


class EnrollmentForm(ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']


class AddTaForm(ModelForm):
    class Meta:
        model = CourseAdministrator
        fields = ['administrator', 'course']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'correct_answer']
