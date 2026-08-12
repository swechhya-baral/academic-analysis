from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Student, Teacher, Course, Enrollment, Grade, Attendance
from .forms import StudentForm, TeacherForm, CourseForm, EnrollmentForm, GradeForm, AttendanceForm


class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    login_url = 'login'


# ---- Student ----
class StudentListView(AdminOnlyMixin, ListView):
    model = Student
    template_name = 'academics/manage/student_list.html'
    context_object_name = 'objects'

class StudentCreateView(AdminOnlyMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_students')
    extra_context = {'title': 'Add Student'}

class StudentUpdateView(AdminOnlyMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_students')
    extra_context = {'title': 'Edit Student'}

class StudentDeleteView(AdminOnlyMixin, DeleteView):
    model = Student
    template_name = 'academics/manage/crud_confirm_delete.html'
    success_url = reverse_lazy('manage_students')


# ---- Teacher ----
class TeacherListView(AdminOnlyMixin, ListView):
    model = Teacher
    template_name = 'academics/manage/teacher_list.html'
    context_object_name = 'objects'

class TeacherCreateView(AdminOnlyMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_teachers')
    extra_context = {'title': 'Add Teacher'}

class TeacherUpdateView(AdminOnlyMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_teachers')
    extra_context = {'title': 'Edit Teacher'}

class TeacherDeleteView(AdminOnlyMixin, DeleteView):
    model = Teacher
    template_name = 'academics/manage/crud_confirm_delete.html'
    success_url = reverse_lazy('manage_teachers')


# ---- Course ----
class CourseListView(AdminOnlyMixin, ListView):
    model = Course
    template_name = 'academics/manage/course_list.html'
    context_object_name = 'objects'

class CourseCreateView(AdminOnlyMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_courses')
    extra_context = {'title': 'Add Course'}

class CourseUpdateView(AdminOnlyMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_courses')
    extra_context = {'title': 'Edit Course'}

class CourseDeleteView(AdminOnlyMixin, DeleteView):
    model = Course
    template_name = 'academics/manage/crud_confirm_delete.html'
    success_url = reverse_lazy('manage_courses')


# ---- Enrollment ----
class EnrollmentListView(AdminOnlyMixin, ListView):
    model = Enrollment
    template_name = 'academics/manage/enrollment_list.html'
    context_object_name = 'objects'

class EnrollmentCreateView(AdminOnlyMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_enrollments')
    extra_context = {'title': 'Add Enrollment'}

class EnrollmentUpdateView(AdminOnlyMixin, UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_enrollments')
    extra_context = {'title': 'Edit Enrollment'}

class EnrollmentDeleteView(AdminOnlyMixin, DeleteView):
    model = Enrollment
    template_name = 'academics/manage/crud_confirm_delete.html'
    success_url = reverse_lazy('manage_enrollments')


# ---- Grade ----
class GradeListView(AdminOnlyMixin, ListView):
    model = Grade
    template_name = 'academics/manage/grade_list.html'
    context_object_name = 'objects'

class GradeCreateView(AdminOnlyMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_grades')
    extra_context = {'title': 'Add Grade'}

class GradeUpdateView(AdminOnlyMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_grades')
    extra_context = {'title': 'Edit Grade'}

class GradeDeleteView(AdminOnlyMixin, DeleteView):
    model = Grade
    template_name = 'academics/manage/crud_confirm_delete.html'
    success_url = reverse_lazy('manage_grades')


# ---- Attendance ----
class AttendanceListView(AdminOnlyMixin, ListView):
    model = Attendance
    template_name = 'academics/manage/attendance_list.html'
    context_object_name = 'objects'

class AttendanceCreateView(AdminOnlyMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_attendance')
    extra_context = {'title': 'Add Attendance'}

class AttendanceUpdateView(AdminOnlyMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'academics/manage/crud_form.html'
    success_url = reverse_lazy('manage_attendance')
    extra_context = {'title': 'Edit Attendance'}

class AttendanceDeleteView(AdminOnlyMixin, DeleteView):
    model = Attendance
    template_name = 'academics/manage/crud_confirm_delete.html'
    success_url = reverse_lazy('manage_attendance')