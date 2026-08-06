from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Teacher, Student, Course, Enrollment, Grade, Attendance
from datetime import date


class ModelTests(TestCase):
    def setUp(self):
        # Runs before every test — sets up common test data
        self.teacher_user = User.objects.create_user(username='teacher_test', password='pass123')
        self.teacher = Teacher.objects.create(user=self.teacher_user, department='CS')

        self.student_user = User.objects.create_user(username='student_test', password='pass123')
        self.student = Student.objects.create(user=self.student_user, roll_number='TEST-01')

        self.course = Course.objects.create(code='CS999', name='Test Course', teacher=self.teacher)

        self.enrollment = Enrollment.objects.create(
            student=self.student, course=self.course, semester='Test Semester'
        )

    def test_student_creation(self):
        self.assertEqual(self.student.roll_number, 'TEST-01')
        self.assertEqual(str(self.student), self.student_user.username)

    def test_enrollment_links_correctly(self):
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.course, self.course)

    def test_grade_average_calculation(self):
        Grade.objects.create(enrollment=self.enrollment, assessment_type='Midterm', score=80, max_score=100)
        Grade.objects.create(enrollment=self.enrollment, assessment_type='Final', score=60, max_score=100)
        grades = Grade.objects.filter(enrollment=self.enrollment)
        avg = sum(g.score for g in grades) / grades.count()
        self.assertEqual(avg, 70)

    def test_attendance_percentage(self):
        Attendance.objects.create(enrollment=self.enrollment, date=date(2026, 8, 1), present=True)
        Attendance.objects.create(enrollment=self.enrollment, date=date(2026, 8, 3), present=False)
        total = Attendance.objects.filter(enrollment=self.enrollment).count()
        present = Attendance.objects.filter(enrollment=self.enrollment, present=True).count()
        self.assertEqual((present / total) * 100, 50)


class ViewTests(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user(username='student_test', password='pass123')
        self.student = Student.objects.create(user=self.student_user, roll_number='TEST-01')

    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_required_for_dashboard(self):
        # Not logged in — redirect to login page
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302)  # 302 = redirect

    def test_student_can_access_own_dashboard(self):
        self.client.login(username='student_test', password='pass123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
