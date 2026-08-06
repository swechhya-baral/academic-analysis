from django import forms
from .models import Grade, Attendance

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['enrollment', 'assessment_type', 'score', 'max_score']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['enrollment', 'date', 'present']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }