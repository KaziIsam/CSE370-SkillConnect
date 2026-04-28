"""
students/forms.py
=================
WHY FORMS?
  Django forms handle:
  1. Rendering HTML form fields automatically
  2. Validating submitted data
  3. Showing error messages

  We keep forms simple here since our templates
  build the HTML manually for full styling control.
  The views.py handles validation directly.
"""

from django import forms
from .models import Student, StudentSkill, Skill, Department


class StudentForm(forms.ModelForm):
    """
    ModelForm: Django automatically creates form fields
    from the model's column definitions.
    """
    class Meta:
        model  = Student
        fields = ['name', 'email', 'phone', 'enrollment_year', 'dept']
        widgets = {
            'name':            forms.TextInput(attrs={'placeholder': 'Full name'}),
            'email':           forms.EmailInput(attrs={'placeholder': 'student@bracu.ac.bd'}),
            'phone':           forms.TextInput(attrs={'placeholder': '01XXXXXXXXX'}),
            'enrollment_year': forms.NumberInput(attrs={'min': 2010, 'max': 2030}),
        }


class StudentSkillForm(forms.ModelForm):
    """Used on the profile page to add a skill to a student."""
    class Meta:
        model  = StudentSkill
        fields = ['skill', 'proficiency_level', 'acquired_date']
        widgets = {
            'acquired_date': forms.DateInput(attrs={'type': 'date'}),
        }