import re
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from buddy.models import Quiz, Question, Answer, Course, CourseAdministrator, Profile
from django.views.generic import edit
from django.shortcuts import redirect
from buddy.forms import AddTaForm
from django.urls import reverse
from django.contrib.auth.models import User


@login_required
def add_student_assistant(request, course_code):
    # Check if the user trying to add is a professor
    if request.method == 'POST':
        #get student objects
        email_adress = request.POST['student_email']
        student = User.objects.filter(email=email_adress).first()
        #get course objects
        course = Course.objects.filter(course_code=course_code).first()
        if request.user.profile.is_professor and CourseAdministrator.objects.filter(administrator=request.user, course=course):
            #ensure both student and course are valid
            if course is None or student is None:
                pass
            #check what is wrong, then return something appropriate
            elif CourseAdministrator.objects.filter(administrator=student, course=course):
                print('The user is already admin in this course. ')
            else:
                #make a new CourseAdmin objects
                ta = CourseAdministrator(administrator=student, course=course)
                #save the object
                ta.save()
            #return the prefered page
            return HttpResponseRedirect(reverse('buddy:get_course_site', kwargs={'course_code': course_code}))
    return HttpResponse('Invalid user. You are either not a professor or you do not have admin rights to this course.')
