import re
from django.shortcuts import render, get_object_or_404, reverse
from django.http import request, HttpResponse, HttpResponseRedirect, Http404, QueryDict
from django.contrib.auth.decorators import login_required
from buddy.models import Quiz, Question, Answer, Course, CourseAdministrator, QuestionIsEditedByTa
from buddy.forms import QuestionForm
from django.views.generic import edit
from django.shortcuts import redirect

@login_required
def question_edit(request, question_id):
    """"
    :param pk: Primary key for a question object
    """
    question = get_object_or_404(Question, QUESTION_ID=question_id)
    quiz = question.quiz
    course = quiz.course

    if CourseAdministrator.objects.filter(course=course, administrator=request.user):
        if request.user.profile.is_professor:
            try:
                QuestionIsEditedByTa.objects.filter(question=question).delete()
            except:
                print('Did not delete anything')
        # If POST-request then update the question text, but the user will continue to edit the question
        if request.method == 'POST':
            if request.user.profile.is_professor:
                question.question_text = request.POST['question_text']
                question.save()
            else:
                # Adds that the ta has changed the question to the database if it's not there already
                if QuestionIsEditedByTa.objects.filter(question=question).first() == None:
                    question.question_text = request.POST['question_text']
                    question.save()
                    ta_edit = QuestionIsEditedByTa(course=course, quiz=quiz, question=question)
                    ta_edit.save()
                # If it is there already, just change the question
                else:
                    question.question_text = request.POST['question_text']
                    question.save()
        question_form = QuestionForm(instance=question)
        answers = get_answers_for_question(question)

        return render(request, 'quiz/question_edit.html', {'form': question_form,
                                                           'answers': answers, 'question': question})
    return HttpResponseRedirect(reverse("buddy:index"))

@login_required
def question_create(request, quiz_id):
    quiz = get_object_or_404(Quiz, QUIZ_ID=quiz_id)
    course = quiz.course

    if CourseAdministrator.objects.filter(course=course, administrator=request.user):
        if request.method == 'POST':
            question = Question(quiz=quiz)
            question.question_text = request.POST['question_text']
            question.save()
            if request.user.profile.is_professor:
                return HttpResponse(reverse("buddy:question-edit", kwargs={"question_id": question.pk}))
            else:
                # Save relation to database
                ta_create = QuestionIsEditedByTa(course=course, quiz=quiz, question=question)
                ta_create.save()
                return HttpResponseRedirect(reverse("buddy:question-edit", kwargs={"question_id": question.pk}))
        question_form = QuestionForm()
        return render(request, 'quiz/question_create.html', {'form': question_form, 'quiz': quiz})
    return HttpResponseRedirect(reverse("buddy:index"))

@login_required
def question_delete(request, question_id):
    question = get_object_or_404(Question, QUESTION_ID=question_id)
    if request.method == 'POST':
        # Delete the question
        question.delete()
        # Redirect to quiz page
        return HttpResponseRedirect(reverse("buddy:quiz-edit", kwargs={"quiz_id": question.quiz.QUIZ_ID}))
    # Return delete page
    return render(request, 'quiz/question_delete.html', {"question": question})


def get_answers_for_question(question):
    answers_query_set = Answer.objects.filter(question=question)
    if not answers_query_set:
        return []
    else:
        return [question for question in answers_query_set]
