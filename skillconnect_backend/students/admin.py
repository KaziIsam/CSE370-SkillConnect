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
    list_display  = ['student_id', 'name', 'email', 'dept', 'enrollment_year']
    list_filter   = ['dept', 'enrollment_year']
    search_fields = ['name', 'email']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ['skill_id', 'skill_name', 'category']
    list_filter   = ['category']

@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):
    list_display  = ['student', 'skill', 'proficiency_level', 'acquired_date']
    list_filter   = ['proficiency_level']

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['club_id', 'club_name', 'founding_year']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['event_id', 'event_name', 'event_date', 'club']

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

admin.site.register(SkillTools)
admin.site.register(ClubMembership)
