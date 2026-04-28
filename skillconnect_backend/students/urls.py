"""
students/urls.py
================
This maps URLs to view functions.

HOW TO READ:
  path('list/', views.student_list, name='student_list')
   ↑              ↑                  ↑
  URL pattern   view function      name (used in templates
                to call           with {% url 'student_list' %})

URL PATTERNS EXPLAINED:
  ''              → /students/          → dashboard
  'list/'         → /students/list/     → all students
  'search/'       → /students/search/   → skill search
  'report/'       → /students/report/   → skill report
  'add/'          → /students/add/      → add student form
  '<int:id>/'     → /students/1/        → student 1 profile
  '<int:id>/delete/' → /students/1/delete/ → delete student 1

<int:student_id>:
  The <int:...> part is a URL parameter.
  Django captures the number from the URL and passes it
  to the view function as student_id argument.
  Example: /students/5/ → student_profile(request, student_id=5)
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',
         views.dashboard,
         name='dashboard'),

    path('list/',
         views.student_list,
         name='student_list'),

    path('student/<int:student_id>/',
         views.student_profile,
         name='student_profile'),

    path('add/',
         views.add_student,
         name='add_student'),

    path('student/<int:student_id>/add-skill/',
         views.add_skill,
         name='add_skill'),

    path('student/<int:student_id>/delete/',
         views.delete_student,
         name='delete_student'),

    path('search/',
         views.skill_search,
         name='skill_search'),

    path('report/',
         views.skill_report,
         name='skill_report'),
]