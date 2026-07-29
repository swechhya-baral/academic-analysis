from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Course, Teacher, Enrollment, Grade, Attendance
from django.db.models import Avg, Count, Q

def home(request):
    if not request.user.is_authenticated:
        student_count = Student.objects.count()
        course_count = Course.objects.count()
        return render(request, 'academics/home.html', {
            'student_count': student_count,
            'course_count': course_count,
        })

    # Logged in — redirect based on role
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    elif hasattr(request.user, 'teacher'):
        return redirect('teacher_dashboard')
    elif hasattr(request.user, 'student'):
        return redirect('student_dashboard')
    else:
        return render(request, 'academics/home.html', {})


@login_required
def student_dashboard(request):
    student = request.user.student
    enrollments = Enrollment.objects.filter(student=student)

    enrollment_data = []
    for e in enrollments:
        grades = Grade.objects.filter(enrollment=e)
        avg_score = grades.aggregate(avg=Avg('score'))['avg'] or 0
        total_sessions = Attendance.objects.filter(enrollment=e).count()
        present_sessions = Attendance.objects.filter(enrollment=e, present=True).count()
        attendance_pct = (present_sessions / total_sessions * 100) if total_sessions else 0

        enrollment_data.append({
            'course': e.course,
            'avg_score': round(avg_score, 2),
            'attendance_pct': round(attendance_pct, 2),
            'grades': grades,
        })

    context = {'student': student, 'enrollment_data': enrollment_data}
    return render(request, 'academics/student_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    teacher = request.user.teacher
    courses = Course.objects.filter(teacher=teacher)

    course_data = []
    for c in courses:
        enrollments = Enrollment.objects.filter(course=c)
        student_count = enrollments.count()
        avg_score = Grade.objects.filter(enrollment__course=c).aggregate(avg=Avg('score'))['avg'] or 0
        course_data.append({
            'course': c,
            'student_count': student_count,
            'avg_score': round(avg_score, 2),
        })

    context = {'teacher': teacher, 'course_data': course_data}
    return render(request, 'academics/teacher_dashboard.html', context)


@login_required
def admin_dashboard(request):
    context = {
        'student_count': Student.objects.count(),
        'course_count': Course.objects.count(),
        'teacher_count': Teacher.objects.count(),
    }
    return render(request, 'academics/admin_dashboard.html', context)