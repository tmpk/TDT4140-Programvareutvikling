from django.test import TestCase
from buddy.models import Course, Enrollment, CourseAdministrator
from django.contrib.auth.models import User


class ModelsTestCase(TestCase):
    def setUp(self):

        # Set up test students
        student1 = User.objects.create_user(username='Student-1', email='user1@stud.ntnu.no', password='psEruWTg')
        student2 = User.objects.create_user(username='Student-2', email='user2@stud.ntnu.no', password='SC33Se9x')
        student3 = User.objects.create_user(username='Student-3', email='user3@stud.ntnu.no', password='LrNffbSN')
        student4 = User.objects.create_user(username='Student-4', email='user4@stud.ntnu.no', password='Zuu3P2F4')
        student5 = User.objects.create_user(username='Student-5', email='user5@stud.ntnu.no', password='bUd2kj55')
        student6 = User.objects.create_user(username='Student-6', email='user6@stud.ntnu.no', password='zpsMtKsw')

        # Set up test professors
        professor1 = User.objects.create_user(username='Professor-1', email='professor1@ntnu.no', password='LxrUJHz9')
        professor1.profile.is_professor = True
        professor1.save()
        professor2 = User.objects.create_user(username='Professor-2', email='professor2@ntnu.no', password='WKQWSaFN')
        professor2.profile.is_professor = True
        professor2.save()
        # Create fake courses
        course1 = Course(course_code='TDT4140', name='Programvareutvikling')
        course1.save()
        course2 = Course(course_code='TDT4180', name='Menneske-maskin interaksjon')
        course2.save()
        course3 = Course(course_code='TTM4100', name='Kommunikasjon- tjenester og nett')
        course3.save()
        course4 = Course(course_code='TDT4145', name='Datamodellering og databasesystemer')
        course4.save()

        # Enroll students in courses
        Enrollment(student=student1, course=course1).save()
        Enrollment(student=student1, course=course2).save()

        # Set professor as course administrator
        CourseAdministrator(administrator=professor1, course=course1).save()
        

    def test_stores_correct_email(self):
        self.assertEqual(User.objects.get_by_natural_key('Student-1').email, 'user1@stud.ntnu.no')

    def test_can_get_enrollments_for_user(self):
        student = User.objects.get_by_natural_key('Student-1')
        users_enrollments = Enrollment.objects.filter(student=student)
        
        users_courses = list()
        for enrollment in users_enrollments:
            users_courses.append(enrollment.course)

        tdt4140 = Course.objects.filter(course_code='TDT4140').get()
        tdt4180 = Course.objects.filter(course_code='TDT4180').get()
        self.assertEqual(users_courses, [tdt4140, tdt4180])

    def test_can_get_courses_professor_administers(self):
        professor = User.objects.get_by_natural_key('Professor-1')
        adminestering = CourseAdministrator.objects.filter(administrator=professor)
        
        teaching = list()
        for admin in adminestering:
            teaching.append(admin.course)

        tdt4140 = Course.objects.filter(course_code='TDT4140').get()
        self.assertEqual(teaching, [tdt4140])