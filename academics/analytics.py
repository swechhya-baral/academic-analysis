from django.db.models import Avg, Count, Q, Case, When, FloatField
from .models import Student, Enrollment, Grade, Attendance


def get_student_risk_data():
    # Returns a list of dicts with each student's average score,attendance % and a computed risk flag.
    
    students = Student.objects.all()
    results = []

    for student in students:
        enrollments = Enrollment.objects.filter(student=student)

        avg_score = Grade.objects.filter(enrollment__in=enrollments).aggregate(
            avg=Avg('score'))['avg'] or 0

        total_att = Attendance.objects.filter(enrollment__in=enrollments).count()
        present_att = Attendance.objects.filter(enrollment__in=enrollments, present=True).count()
        attendance_pct = (present_att / total_att * 100) if total_att else 0

        # Simple rule-based risk flag 
        is_at_risk = avg_score < 60 or attendance_pct < 75

        results.append({
            'student': student,
            'avg_score': round(avg_score, 2),
            'attendance_pct': round(attendance_pct, 2),
            'is_at_risk': is_at_risk,
        })

    return results