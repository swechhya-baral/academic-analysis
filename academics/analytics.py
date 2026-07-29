import os
import joblib
from django.conf import settings
from .models import Student, Enrollment, Grade, Attendance
from django.db.models import Avg

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml', 'risk_model.pkl')
_model = None


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def get_student_risk_data():
    model = get_model()
    students = Student.objects.all()
    results = []

    for student in students:
        enrollments = Enrollment.objects.filter(student=student)

        avg_score = Grade.objects.filter(enrollment__in=enrollments).aggregate(
            avg=Avg('score'))['avg'] or 0

        total_att = Attendance.objects.filter(enrollment__in=enrollments).count()
        present_att = Attendance.objects.filter(enrollment__in=enrollments, present=True).count()
        attendance_pct = (present_att / total_att * 100) if total_att else 0

        avg_score = float(avg_score)
        attendance_pct = float(attendance_pct)

        prediction = model.predict([[avg_score, attendance_pct]])[0]
        is_at_risk = bool(prediction)

        results.append({
            'student': student,
            'avg_score': round(avg_score, 2),
            'attendance_pct': round(attendance_pct, 2),
            'is_at_risk': is_at_risk,
        })

    return results