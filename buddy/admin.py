from django.contrib import admin

# Import models
from .models import Course, CourseAdministrator, Enrollment
# Register your models here.

admin.site.register(Course)
admin.site.register(CourseAdministrator)
admin.site.register(Enrollment)
