from django.contrib.auth.models import User
from buddy.models import Course, Enrollment, CourseAdministrator, Quiz, Question, Answer


def seed():

    # Set up test students
    student1 = User.objects.create_user(
        username='Student-1', email='user1@stud.ntnu.no', password='psEruWTg')
    student1.save()
    student2 = User.objects.create_user(
        username='Student-2', email='user2@stud.ntnu.no', password='SC33Se9x')
    student2.save()
    student3 = User.objects.create_user(
        username='Student-3', email='user3@stud.ntnu.no', password='LrNffbSN')
    student3.save()
    student4 = User.objects.create_user(
        username='Student-4', email='user4@stud.ntnu.no', password='Zuu3P2F4')
    student4.save()
    student5 = User.objects.create_user(
        username='Student-5', email='user5@stud.ntnu.no', password='bUd2kj55')
    student5.save()
    student6 = User.objects.create_user(
        username='Student-6', email='user6@stud.ntnu.no', password='zpsMtKsw')
    student6.save()

    # Set up test professors
    professor1 = User.objects.create_user(
        username='Professor-1', email='professor1@ntnu.no', password='LxrUJHz9')
    professor1.profile.is_professor = True
    professor1.save()
    professor2 = User.objects.create_user(
        username='Professor-2', email='professor2@ntnu.no', password='WKQWSaFN')
    professor2.profile.is_professor = True
    professor2.save()

    # Create fake courses
    course1 = Course(course_code='TDT4120',
                     name='Algoritmer og datastrukturer')
    course1.save()
    course2 = Course(course_code='TMA4100', name='Matematikk 1')
    course2.save()
    course3 = Course(course_code='TTM4100',
                     name='Kommunikasjon- tjenester og nett')
    course3.save()
    course4 = Course(course_code='TDT4145',
                     name='Datamodellering og databasesystemer')
    course4.save()

    # create fake quizzes
    quiz1 = Quiz(course=course1, name='Comparison sorts', due_date='2018-03-26 23:59')
    quiz1.save()
    quiz3 = Quiz(course=course1, name='P vs. NP', due_date='2018-03-26 23:59')
    quiz3.save()
    quiz2 = Quiz(course=course2, name='Kontinuitet og derivasjon', due_date='2018-04-07 12:00')
    quiz2.save()

    # questions and answers to quizzes
    question1quiz1 = Question(
        quiz=quiz1, question_text='Hva er average-case kjøretid for Quicksort?')
    question1quiz1.save()
    answer1question1quiz1 = Answer(
        question=question1quiz1, answer_text='O(log(n))', correct_answer=False)
    answer1question1quiz1.save()
    answer2question1quiz1 = Answer(
        question=question1quiz1, answer_text='O(n(log(n)))', correct_answer=True)
    answer2question1quiz1.save()
    answer3question1quiz1 = Answer(
        question=question1quiz1, answer_text='O(n)', correct_answer=False)
    answer3question1quiz1.save()

    question2quiz1 = Question(
        quiz=quiz1, question_text='Kan man i det generelle tilfellet garantere at en comparison sort har en average-case kjøretid bedre enn O(n(log(n)))?')
    question2quiz1.save()
    answer1question2quiz1 = Answer(
        question=question2quiz1, answer_text='Nei.', correct_answer=True)
    answer1question2quiz1.save()
    answer2question2quiz1 = Answer(
        question=question2quiz1, answer_text='Ja.', correct_answer=False)
    answer2question2quiz1.save()
    answer3question2quiz1 = Answer(
        question=question2quiz1, answer_text='Bare på tirsdag.', correct_answer=False)
    answer3question2quiz1.save()

    question1quiz2 = Question(
        quiz=quiz2, question_text='Hvilke av følgende utsagn er sanne?', multiple_correct_answers=True)
    question1quiz2.save()
    answer1question1quiz2 = Answer(
        question=question1quiz2, answer_text='Dersom en funksjon f(x) er deriverbar i et punkt, må den også være kontinuerlig her.', correct_answer=True)
    answer1question1quiz2.save()
    answer2question1quiz2 = Answer(
        question=question1quiz2, answer_text='Dersom en funksjon f(x) er kontinuerlig i et punkt, må den også være deriverbar her.', correct_answer=False)
    answer2question1quiz2.save()
    answer3question1quiz2 = Answer(
        question=question1quiz2, answer_text='Dersom en funksjon f(x) er diskontinuerlig i et punkt, kan den ikke være deriverbar her', correct_answer=True)
    answer3question1quiz2.save()
    answer4question1quiz2 = Answer(
        question=question1quiz2, answer_text='Dersom en funksjon f(x) ikke er er deriverbar i et punkt, kan den ikke være kontinuerlig her', correct_answer=False)
    answer4question1quiz2.save()

    question2quiz2 = Question(quiz=quiz2, question_text='Eksisterer grensen lim(x->0) (sin(x)/x)?')
    question2quiz2.save()
    answer1question2quiz2=Answer(question=question2quiz2, answer_text="Ja.", correct_answer=True)
    answer1question2quiz2.save()
    answer2question2quiz2=Answer(question=question2quiz2, answer_text="Nei", correct_answer=False)
    answer2question2quiz2.save()



    question1quiz3 = Question(
        quiz=quiz3, question_text='La A være i P, B i NPC og C i NP. For å vise at P=NP må man (i polynomisk tid) redusere:')
    question1quiz3.save()
    answer1question1quiz3 = Answer(
        question=question1quiz3, answer_text='A til B', correct_answer=False
    )
    answer1question1quiz3.save()
    answer2question1quiz3 = Answer(
        question=question1quiz3, answer_text='B til A', correct_answer=True
    )
    answer2question1quiz3.save()
    answer3question1quiz3 = Answer(
        question=question1quiz3, answer_text='A til C', correct_answer=False
    )
    answer3question1quiz3.save()
    answer4question1quiz3 = Answer(
        question=question1quiz3, answer_text='C til A', correct_answer=False
    )
    answer4question1quiz3.save()
    answer5question1quiz3 = Answer(
        question=question1quiz3, answer_text='Det er umulig å vise', correct_answer=False)
    answer5question1quiz3.save()

    # Enroll students in courses
    Enrollment(student=student1, course=course1).save()
    Enrollment(student=student1, course=course2).save()
    Enrollment(student=student1, course=course3).save()
    Enrollment(student=student2, course=course4).save()
    Enrollment(student=student3, course=course2).save()

    # Set professor as course administrator
    CourseAdministrator(administrator=professor1, course=course1).save()
    CourseAdministrator(administrator=professor1, course=course2).save()
    CourseAdministrator(administrator=professor1, course=course3).save()
    CourseAdministrator(administrator=professor1, course=course4).save()

    # Make students ta
    CourseAdministrator(administrator=student1, course=course1).save()
    CourseAdministrator(administrator=student1, course=course2).save()
