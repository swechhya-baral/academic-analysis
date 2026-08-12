from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('grade/add/', views.add_grade, name='add_grade'),
    path('attendance/add/', views.add_attendance, name='add_attendance'),
]

from .crud_views import (
    StudentListView, StudentUpdateView, StudentDeleteView,
    TeacherListView, TeacherUpdateView, TeacherDeleteView,
    CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    EnrollmentListView, EnrollmentCreateView, EnrollmentUpdateView, EnrollmentDeleteView,
    GradeListView, GradeCreateView, GradeUpdateView, GradeDeleteView,
    AttendanceListView, AttendanceCreateView, AttendanceUpdateView, AttendanceDeleteView,
)

urlpatterns += [
    path('manage/', views.manage_hub, name='manage_hub'),

    path('manage/students/', StudentListView.as_view(), name='manage_students'),
    path('manage/students/add/', views.add_student, name='student_add'),
    path('manage/students/<int:pk>/edit/', StudentUpdateView.as_view(), name='student_edit'),
    path('manage/students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),

    path('manage/teachers/', TeacherListView.as_view(), name='manage_teachers'),
    path('manage/teachers/add/', views.add_teacher, name='teacher_add'),
    path('manage/teachers/<int:pk>/edit/', TeacherUpdateView.as_view(), name='teacher_edit'),
    path('manage/teachers/<int:pk>/delete/', TeacherDeleteView.as_view(), name='teacher_delete'),

    path('manage/courses/', CourseListView.as_view(), name='manage_courses'),
    path('manage/courses/add/', CourseCreateView.as_view(), name='course_add'),
    path('manage/courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('manage/courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    path('manage/enrollments/', EnrollmentListView.as_view(), name='manage_enrollments'),
    path('manage/enrollments/add/', EnrollmentCreateView.as_view(), name='enrollment_add'),
    path('manage/enrollments/<int:pk>/edit/', EnrollmentUpdateView.as_view(), name='enrollment_edit'),
    path('manage/enrollments/<int:pk>/delete/', EnrollmentDeleteView.as_view(), name='enrollment_delete'),

    path('manage/grades/', GradeListView.as_view(), name='manage_grades'),
    path('manage/grades/add/', GradeCreateView.as_view(), name='grade_add'),
    path('manage/grades/<int:pk>/edit/', GradeUpdateView.as_view(), name='grade_edit'),
    path('manage/grades/<int:pk>/delete/', GradeDeleteView.as_view(), name='grade_delete'),

    path('manage/attendance/', AttendanceListView.as_view(), name='manage_attendance'),
    path('manage/attendance/add/', AttendanceCreateView.as_view(), name='attendance_add'),
    path('manage/attendance/<int:pk>/edit/', AttendanceUpdateView.as_view(), name='attendance_edit'),
    path('manage/attendance/<int:pk>/delete/', AttendanceDeleteView.as_view(), name='attendance_delete'),
]