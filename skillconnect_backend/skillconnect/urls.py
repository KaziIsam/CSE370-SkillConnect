"""
skillconnect/urls.py
====================
This is the MAIN URL router for the entire project.
 
HOW URLS WORK IN DJANGO:
  Browser types: http://127.0.0.1:8000/students/
                                         ↑
  Django reads this and says:
  "Does 'students/' match anything in urlpatterns?"
  YES → hand off to students/urls.py to handle the rest.
 
Think of this file as a hotel receptionist:
  - Guest arrives asking for "students" → sent to students floor
  - Guest arrives asking for "admin"    → sent to admin floor
"""
 
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
    path('', include('students.urls')),
]