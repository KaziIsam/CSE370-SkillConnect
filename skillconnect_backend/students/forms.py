from django import forms
from .models import Student, StudentSkill

class StudentForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = ['name', 'email', 'phone', 'enrollment_year', 'dept']

class StudentSkillForm(forms.ModelForm):
    class Meta:
        model  = StudentSkill
        fields = ['skill', 'proficiency_level', 'acquired_date']
        widgets = {'acquired_date': forms.DateInput(attrs={'type': 'date'})}
