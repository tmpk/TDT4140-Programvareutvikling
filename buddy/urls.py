from django.conf.urls import url
from . import views
from buddy.view import login_views, logout_views, quiz_views, question_views, professor_views, answer_views


app_name = 'buddy'
urlpatterns = [
    #General URLs
    url(r'^logout', logout_views.log_out, name='logout'),
    url(r'^(?P<course_code>[A-Z]+[0-9]{4})', views.get_course_site, name='get_course_site'),
    url(r'^database/seed', views.seed_database),

    #URLs related to quizzes
    url(r'^quiz/(?P<course_id>[0-9]+)/add', quiz_views.quiz_create, name='quiz-create'),
    url(r'^quiz/(?P<quiz_id>[0-9]+)/edit', quiz_views.quiz_edit, name='quiz-edit'),
    url(r'^quiz/(?P<quiz_id>[0-9]+)/delete', quiz_views.quiz_delete, name='quiz-delete'),
    url(r'^quiz/(?P<quiz_id>[0-9]+)/reviewresults', views.reviewresults, name='reviewresults'),
    url(r'^quiz/(?P<quiz_id>[0-9]+)/results', views.results, name='results'),
    url(r'^quiz/(?P<quiz_id>[0-9]+)/xaxa', views.prof_results, name='prof-results'),
    url(r'^quiz/(?P<quiz_id>[0-9]+)', views.quiz_student, name='quiz_student'),

    #URLs related to questions
    url(r'^question/add/(?P<quiz_id>[0-9]+)', question_views.question_create, name='question-add'),
    url(r'^question/(?P<question_id>[0-9]+)/edit', question_views.question_edit, name='question-edit'),
    url(r'^question/(?P<question_id>[0-9]+)/delete', question_views.question_delete, name='question-delete'),

    #URLs related to answers
    url(r'^answer/(?P<question_id>[0-9]+)/add', answer_views.answer_create, name='answer-create'),
    url(r'^answer/(?P<answer_id>[0-9]+)/edit', answer_views.answer_edit, name='answer-edit'),
    url(r'^answer/(?P<answer_id>[0-9]+)/delete', answer_views.answer_delete, name='answer-delete'),

    #URLs related to professors
    url(r'^professor/addSubject', views.add_subject, name='addsubject'),
    url(r'^course/(?P<coursecode>[a-zA-Z]{3}[0-9]{4})', views.coursecode, name='student-course-page'),
    url(r'^course/(?P<coursecode>[a-zA-Z]{3}[0-9]{4})', views.coursecode, name='coursecode'),
    url(r'^add_ta/(?P<course_code>[A-Z]+[0-9]{4})', professor_views.add_student_assistant, name='add-ta'),

    url(r'^student/enroll', views.enroll_in_course, name="enroll"),

    url(r'^account/register', login_views.register_view, name='register'),
    url(r'^account/login', login_views.login_view, name='login'),
    url(r'^', views.index, name='index'),
]
