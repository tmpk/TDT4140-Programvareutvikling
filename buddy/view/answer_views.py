import re
from django.shortcuts import render, get_object_or_404, reverse
from django.http import request, HttpResponseRedirect, Http404, QueryDict, HttpResponse
from django.contrib.auth.decorators import login_required
from buddy.models import Quiz, Question, Answer, Course, QuestionIsEditedByTa
from buddy.forms import AnswerForm
from django.views.generic import edit
from django.shortcuts import redirect

@login_required
def answer_create(request, question_id):
    question = get_object_or_404(Question, QUESTION_ID=question_id)
    quiz = question.quiz
    course = quiz.course

    if request.method == 'POST':

        form = AnswerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_answer = form.save(commit=False)
            new_answer.question = question
            new_answer.save()
            # redirect to a new URL:
            # Chechs if user is professor
            if request.user.profile.is_professor:
                return HttpResponseRedirect(reverse("buddy:question-edit", kwargs={"question_id": question.pk}))
            else:
                # Add relation to database
                if QuestionIsEditedByTa.objects.filter(question=question).first() == None:
                    ta_edit = QuestionIsEditedByTa(course=course, quiz=quiz, question=question)
                    ta_edit.save()
                return HttpResponseRedirect(reverse("buddy:question-edit", kwargs={"question_id": question.pk}))
        else:
            # Return error
            pass
    answer_form = AnswerForm()
    return render(request, 'quiz/answer_create.html', {'form': answer_form, 'question': question})

@login_required
def answer_edit(request, answer_id):
    answer = get_object_or_404(Answer, ANSWER_ID=answer_id)
    question = answer.question
    quiz = question.quiz
    course = quiz.course

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            answer = form.save()
            # redirect to a new URL:
            if request.user.profile.is_professor:
                return HttpResponseRedirect(reverse("buddy:question-edit", kwargs={"question_id": answer.question.pk}))
            else:
                # Create relation in database if not already existing
                if QuestionIsEditedByTa.objects.filter(question=question).first() == None:
                    print('added to database')
                    ta_edit = QuestionIsEditedByTa(course=course, quiz=quiz, question=question)
                    ta_edit.save()
                print('not added')
                return HttpResponseRedirect(reverse("buddy:question-edit", kwargs={"question_id": answer.question.pk}))
        else:
            # Return error
            pass
    answer_form = AnswerForm(instance=answer)
    return render(request, 'quiz/answer_edit.html', {'form': answer_form, 'question': answer.question})

@login_required
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, ANSWER_ID=answer_id)

    if request.method == 'POST':
        # Delete the question
        answer.delete()
        # Redirect to quiz page
        return HttpResponseRedirect(reverse("buddy:question-edit", kwargs={"question_id": answer.question.pk}))
    # Return delete page
    return render(request, 'quiz/answer_delete.html', {"answer": answer})
