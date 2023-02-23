import re
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, ValidationError
from buddy.models import Quiz, Question, Course, CourseAdministrator, QuizIsCreatedByTa
from buddy.forms import  QuizForm

@login_required
def quiz_create(request, course_id):
    course = get_object_or_404(Course, COURSE_ID=course_id)
    # Check if the user is an admin for this course
    if CourseAdministrator.objects.filter(administrator=request.user, course=course):
        if request.method == 'POST':
            form = QuizForm(request.POST)
            new_quiz = form.save(commit=False)
            new_quiz.course = course
            new_quiz.save()

            # redirect to a new URL:
            if request.user.profile.is_professor:
                return HttpResponseRedirect(reverse("buddy:quiz-edit", kwargs={"quiz_id": new_quiz.pk}))
            else:
                # Creates a relation in the database
                ta_create = QuizIsCreatedByTa(course=course, quiz=new_quiz)
                ta_create.save()
                return HttpResponseRedirect(reverse("buddy:quiz-edit", kwargs={"quiz_id": new_quiz.pk}))
        #else:
            #Return error
            pass
        quiz = Quiz(course=course)
        quiz_form = QuizForm(instance=quiz)
        return render(request, 'quiz/quiz_create.html', {'form': quiz_form, 'course': course})
    return HttpResponse('Invalid user. You do not have admin rights to this course.')


@login_required
def quiz_edit(request, quiz_id):
    course = Quiz.objects.filter(QUIZ_ID=quiz_id).first().course
    quiz = get_object_or_404(Quiz, QUIZ_ID=quiz_id)
    # If the professor sees the quiz, remove the quiz from notifications
    if request.user.profile.is_professor:
        try:
            QuizIsCreatedByTa.objects.filter(quiz=quiz).delete()
        except:
            print('Did not delete anything')
    # Check if the user is an admin for this course
    if CourseAdministrator.objects.filter(administrator=request.user, course=course):

        if request.method == 'POST':
            form = QuizForm(request.POST, instance=quiz)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                quiz = form.save()
                # redirect to a new URL:
                return HttpResponseRedirect(reverse("buddy:quiz-edit", kwargs={"quiz_id": quiz.pk}))
            else:
                # Return error
                pass

        quiz_form = QuizForm(instance=quiz)
        questions = get_questions_for_quiz(quiz)
        return render(request, 'quiz/quiz_edit.html', {'form': quiz_form, 'quiz': quiz, 'questions': questions})
    return HttpResponse('Invalid user. You are either not a professor or you do not have admin rights to this course.')


@login_required
def quiz_delete(request, quiz_id):
    course = Quiz.objects.filter(QUIZ_ID=quiz_id).first()
    quiz = get_object_or_404(Quiz, QUIZ_ID=quiz_id)
    # Check if the user is an admin for this course
    if CourseAdministrator.objects.filter(administrator=request.user, course=course.course):
        if request.method == 'POST':
            # Delete
            quiz.delete()
            return HttpResponseRedirect(reverse('buddy:get_course_site', kwargs={'course_code': quiz.course.course_code}))
        return render(request, 'quiz/quiz_delete.html', {'quiz': quiz})
    return HttpResponse('Invalid user. You are either not a professor or you do not have admin rights to this course.')


def get_questions_for_quiz(quiz):
    questions_query_set = Question.objects.filter(quiz=quiz)
    if not questions_query_set:
        return []
    else:
        return [question for question in questions_query_set]
