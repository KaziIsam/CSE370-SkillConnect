"""
students/admin.py
=================
WHY ADMIN?
  Django gives you a FREE admin panel at /admin/
  where you can view, add, edit, delete database records
  without writing any code.

  Just register your models here and it works automatically.
  Great for quickly checking your data during development.

HOW TO ACCESS:
  1. Run: python manage.py createsuperuser
  2. Follow prompts to set username + password
  3. Visit: http://127.0.0.1:8000/admin/
  4. Login with your superuser credentials
"""

from django.contrib import admin
from .models import (
    Department, Student, Skill, SkillTools,
    StudentSkill, Club, Event, Participation,
    ClubMembership, UndergradStudent, GradStudent
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display  = ['dept_id', 'dept_code', 'dept_name']
    search_fields = ['dept_name', 'dept_code']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display   = ['student_id', 'name', 'email', 'dept', 'enrollment_year']
    list_filter    = ['dept', 'enrollment_year']
    search_fields  = ['name', 'email']
    # list_filter adds dropdown filters in the right sidebar
    # search_fields adds a search box at the top


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ['skill_id', 'skill_name', 'category']
    list_filter   = ['category']
    search_fields = ['skill_name']


@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):
    list_display  = ['student', 'skill', 'proficiency_level', 'acquired_date']
    list_filter   = ['proficiency_level']
    search_fields = ['student__name', 'skill__skill_name']
    # student__name = follow FK to Student and search by name


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['club_id', 'club_name', 'founding_year']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['event_id', 'event_name', 'event_date', 'club', 'max_participants']
    list_filter  = ['club']


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['student', 'event', 'status', 'registration_date']
    list_filter  = ['status']


@admin.register(UndergradStudent)
class UndergradAdmin(admin.ModelAdmin):
    list_display = ['student', 'cgpa', 'credit_completed', 'year_of_study']


@admin.register(GradStudent)
class GradAdmin(admin.ModelAdmin):
    list_display = ['student', 'supervisor', 'research_area']


# Simple registrations (no custom display needed)
admin.site.register(SkillTools)
admin.site.register(ClubMembership)