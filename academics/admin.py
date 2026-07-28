from django.contrib import admin

from .models import Teacher, Student, Course, Enrollment, Grade, Attendance

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Grade)
admin.site.register(Attendance)