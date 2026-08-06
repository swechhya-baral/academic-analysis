from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student, Course, Teacher, Enrollment, Grade, Attendance
from django.db.models import Avg, Count, Q
from .analytics import get_model
from .analytics import get_student_risk_data

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
    model = get_model()

    enrollment_data = []
    for e in enrollments:
        grades = Grade.objects.filter(enrollment=e)
        avg_score = grades.aggregate(avg=Avg('score'))['avg'] or 0

        attendance_records = Attendance.objects.filter(enrollment=e).order_by('date')
        total_sessions = attendance_records.count()
        present_sessions = attendance_records.filter(present=True).count()
        attendance_pct = (present_sessions / total_sessions * 100) if total_sessions else 0

        class_avg = Grade.objects.filter(enrollment__course=e.course).aggregate(avg=Avg('score'))['avg'] or 0

        avg_score = float(avg_score)
        attendance_pct = float(attendance_pct)
        is_at_risk = bool(model.predict([[avg_score, attendance_pct]])[0])

        enrollment_data.append({
            'course': e.course,
            'avg_score': round(avg_score, 2),
            'class_avg': round(float(class_avg), 2),
            'attendance_pct': round(attendance_pct, 2),
            'grades': grades,
            'attendance_records': attendance_records,
            'is_at_risk': is_at_risk,
        })

    context = {'student': student, 'enrollment_data': enrollment_data}
    return render(request, 'academics/student_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    teacher = request.user.teacher
    courses = Course.objects.filter(teacher=teacher)
    model = get_model()

    course_data = []
    for c in courses:
        enrollments = Enrollment.objects.filter(course=c)
        roster = []
        for e in enrollments:
            avg_score = Grade.objects.filter(enrollment=e).aggregate(avg=Avg('score'))['avg'] or 0
            total_att = Attendance.objects.filter(enrollment=e).count()
            present_att = Attendance.objects.filter(enrollment=e, present=True).count()
            attendance_pct = (present_att / total_att * 100) if total_att else 0

            avg_score = float(avg_score)
            attendance_pct = float(attendance_pct)
            is_at_risk = bool(model.predict([[avg_score, attendance_pct]])[0])

            roster.append({
                'student': e.student,
                'avg_score': round(avg_score, 2),
                'attendance_pct': round(attendance_pct, 2),
                'is_at_risk': is_at_risk,
            })

        course_avg = Grade.objects.filter(enrollment__course=c).aggregate(avg=Avg('score'))['avg'] or 0
        course_data.append({
            'course': c,
            'student_count': enrollments.count(),
            'avg_score': round(float(course_avg), 2),
            'roster': roster,
        })

    context = {'teacher': teacher, 'course_data': course_data}
    return render(request, 'academics/teacher_dashboard.html', context)

import json

@login_required
def admin_dashboard(request):
    risk_data = get_student_risk_data()
    at_risk_count = sum(1 for r in risk_data if r['is_at_risk'])

    # Data for charts
    student_names = [r['student'].user.get_full_name() or r['student'].user.username for r in risk_data]
    avg_scores = [r['avg_score'] for r in risk_data]
    attendance_pcts = [r['attendance_pct'] for r in risk_data]

    context = {
        'student_count': Student.objects.count(),
        'course_count': Course.objects.count(),
        'teacher_count': Teacher.objects.count(),
        'risk_data': risk_data,
        'at_risk_count': at_risk_count,
        'student_names': json.dumps(student_names),
        'avg_scores': json.dumps(avg_scores),
        'attendance_pcts': json.dumps(attendance_pcts),
        'risk_labels': json.dumps(['At Risk', 'OK']),
        'risk_counts': json.dumps([at_risk_count, len(risk_data) - at_risk_count]),
    }
    return render(request, 'academics/admin_dashboard.html', context)

from .forms import GradeForm, AttendanceForm
from .models import Enrollment

@login_required
def add_grade(request):
    teacher = request.user.teacher
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = GradeForm()
    # Restrict enrollment choices to this teacher's courses only
    form.fields['enrollment'].queryset = Enrollment.objects.filter(course__teacher=teacher)
    return render(request, 'academics/add_grade.html', {'form': form})


@login_required
def add_attendance(request):
    teacher = request.user.teacher
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = AttendanceForm()
    form.fields['enrollment'].queryset = Enrollment.objects.filter(course__teacher=teacher)
    return render(request, 'academics/add_attendance.html', {'form': form})