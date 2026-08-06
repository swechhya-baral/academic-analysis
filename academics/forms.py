from django import forms
from .models import Grade, Attendance

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['enrollment', 'assessment_type', 'score', 'max_score']
        widgets = {
            'enrollment': forms.Select(attrs={'class': 'form-select'}),
            'assessment_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Midterm'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['enrollment', 'date', 'present']
        widgets = {
            'enrollment': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }