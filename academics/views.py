from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Course, Teacher, Enrollment, Grade, Attendance


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
    context = {
        'student': student,
        'enrollments': enrollments,
    }
    return render(request, 'academics/student_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    teacher = request.user.teacher
    courses = Course.objects.filter(teacher=teacher)
    context = {
        'teacher': teacher,
        'courses': courses,
    }
    return render(request, 'academics/teacher_dashboard.html', context)


@login_required
def admin_dashboard(request):
    context = {
        'student_count': Student.objects.count(),
        'course_count': Course.objects.count(),
        'teacher_count': Teacher.objects.count(),
    }
    return render(request, 'academics/admin_dashboard.html', context)