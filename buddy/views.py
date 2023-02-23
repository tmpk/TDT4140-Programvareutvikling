from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import Context, loader
from .forms import CourseForm, EnrollmentForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Course, CourseAdministrator, Enrollment, Quiz, Question, Answer, CompletedQuestion, CompletedQuiz
from .common import database_seed
from django.shortcuts import get_object_or_404
from datetime import datetime
from buddy.common import database_seed
from django.contrib.auth.models import User
from django.db import models


@login_required
def index(request):
    if request.user.profile.is_professor:
        course = CourseAdministrator.objects.filter(administrator=request.user)
        # If the user is a professor, return the professor view
        return render(request, 'professor/professor.html', {"courses": course})
    else:
        courses = get_students_courses(request.user)
        all_courses = get_all_courses()
        all_upcoming_quizzes = get_all_upcoming_quizzes(request)
        return render(request, 'student/student.html', {"enrolled_courses": courses,
                                                        "all_courses": all_courses,
                                                        "all_upcoming_quizzes": all_upcoming_quizzes})


def get_all_upcoming_quizzes(request):
    all_upcoming_quizzes = []
    courses = get_students_courses(request.user)
    for c in courses:
        all_upcoming_quizzes.extend(
            get_upcoming_quizzes(request, c.course_code))
    return all_upcoming_quizzes

    
@login_required
def add_subject(request):
    if request.user.profile.is_professor:
        if request.method == 'POST':
            course_form = CourseForm(request.POST)
            if course_form.is_valid():
                course = course_form.save()
                course_admin = CourseAdministrator(
                    administrator=request.user, course=course)
                course_admin.save()
            return HttpResponseRedirect(reverse('buddy:index'))
    else:
        pass
    return HttpResponseRedirect(reverse('buddy:index'))


@login_required
def coursecode(request, coursecode):
    course = Course.objects.filter(course_code=coursecode).get()
    quiz = Quiz.objects.all()
    upcoming_quizzes = get_upcoming_quizzes(request, coursecode)
    completed_quizzes = get_completed_quizzes(request, coursecode)
    all_upcoming_quizzes = get_all_upcoming_quizzes(request)
    if (CourseAdministrator.objects.filter(course=course, administrator=request.user).first()) == None:
        is_ta = False
    else:
        is_ta = True
    context = {
        'quiz': quiz,
        'enr_course': coursecode,
        'course': course,
        'is_ta': is_ta,
        'completed_quizzes': completed_quizzes,
        'upcoming_quizzes': upcoming_quizzes,
        'all_upcoming_quizzes': all_upcoming_quizzes
    }
    coursecode = loader.get_template('student/course_page.html')
    return render(request, 'student/course_page.html', context)


@login_required
def quiz_student(request, quiz_id):
    quiz = Quiz.objects.get(QUIZ_ID=quiz_id)
    questions = Question.objects.filter(quiz_id=quiz_id)
    answers = Answer.objects.all()
    quiz_student = loader.get_template('student/quiz_student.html')
    context = {
        'questions': questions,
        'answers': answers,
        'quiz_id': quiz_id,
        'quiz': quiz
    }
    return render(request, 'student/quiz_student.html', context)


def submit(request, quiz_id):
    return HttpResponseRedirect(reverse('buddy:results', args=(quiz_id,)))


@login_required
def results(request, quiz_id):
    if request.method == 'POST':
        results = loader.get_template('student/results.html')
        answers = Answer.objects.all(question__quiz=quiz_id)
        questions = Question.objects.filter(quiz_id=quiz_id)
        completedquestions = []
        newCompletedQuiz = CompletedQuiz(quiz_id=quiz_id, student_id=request.user)
        newCompletedQuiz.save()
        for q in questions:
            givenanswers = request.POST.getlist(str(q.QUESTION_ID))
            for a in givenanswers:
                ans = Answer.objects.get(pk=a)
                newCompletedQuestion = CompletedQuestion(completed_quiz=newCompletedQuiz, q_id=q, given_answer=ans,
                                                         cq_text=q.question_text, mca=q.multiple_correct_answers,
                                                         correct_a=ans.correct_answer)
                newCompletedQuestion.save()
                completedquestions.append(newCompletedQuestion)
        context = {
            'questions': questions,
            'answers': answers,
            'quiz_id': quiz_id,
            'completedquestions': completedquestions
        }
        return render(request, 'student/results.html', context)
    else:
        return HttpResponseRedirect(reverse('buddy:reviewresults', kwargs={'quiz_id': quiz_id}))


def reviewresults(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    completedquiz = CompletedQuiz.objects.get(
        quiz=quiz, student_id=request.user)
    completedquestions = list(
        CompletedQuestion.objects.filter(completed_quiz=completedquiz))
    answers = Answer.objects.filter(question__quiz=quiz)
    context = {
        'answers': answers,
        'quiz_id': quiz_id,
        'completedquestions': completedquestions
    }
    return render(request, 'student/results.html', context)


@login_required
def enroll_in_course(request):
    if request.method == 'POST':
        course_code = request.POST['course']
        if is_course_code_valid(course_code):
            course = get_course_by_course_code(course_code)
            enrollment = Enrollment(course=course, student=request.user)
            enrollment.save()
        return HttpResponseRedirect(reverse('buddy:index'))
    else:
        pass
    return HttpResponseRedirect(reverse('buddy:index'))

def seed_database(request):
    database_seed.seed()
    return HttpResponse("Database seeded")

def get_students_courses(student: User):
    courses = Course.objects.filter(enrollment__student=student)
    if courses:
        return list(courses)
    else:
        return []

def get_all_courses():
    try:
        return Course.objects.all()
    except Exception as e:
        print("Did not get all courses")
        return []


def is_course_code_valid(course_code):
    if Course.objects.filter(course_code=course_code):
        return True
    else:
        return False


def get_course_by_course_code(course_code):
    return Course.objects.get(course_code=course_code)


@login_required
def get_course_site(request, course_code):
    upcoming_quiz_list = get_upcoming_quizzes(request, course_code)
    completed_quiz_list = get_completed_quizzes(request, course_code)
    course = get_course_by_course_code(course_code)
    teaching_assistants = get_teaching_assistants_for_course(course)
    return render(request, 'professor/course_page.html', {"course_code": course_code,
                                                          "course": course,
                                                          "upcoming_quiz_list": upcoming_quiz_list,
                                                          "completed_quiz_list": completed_quiz_list,
                                                          "teaching_assistants": teaching_assistants})

# get upcoming quizzes by course code for a given student
def get_upcoming_quizzes(request, course_code):
    course = get_course_by_course_code(course_code)
    completed_quizzes = get_completed_quizzes(request, course_code)
    quiz_list = ((Quiz.objects.filter(
        course=course, due_date__gte=datetime.now())).exclude(name__in=completed_quizzes))
    if quiz_list:
        return list(quiz_list)
    else:
        return []

# get completed quizzes by course code for a given student
def get_completed_quizzes(request, course_code):
    course = get_course_by_course_code(course_code)
    completed_quizzes = CompletedQuiz.objects.filter(
        student_id=request.user, quiz__course=course).values('quiz')
    quiz_list = (Quiz.objects.filter(QUIZ_ID__in=completed_quizzes))
    if quiz_list:
        return list(quiz_list)
    else:
        return []


def get_teaching_assistants_for_course(course: Course):
    course_admins = User.objects.filter(courseadministrator__course=course)
    course_admins = course_admins.filter(profile__is_professor=False)
    if course_admins:
        return list(course_admins)
    else:
        return []
