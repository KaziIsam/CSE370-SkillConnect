from django.urls import path
from . import views

urlpatterns = [
    path('',                                        views.dashboard,        name='dashboard'),
    path('list/',                                   views.student_list,     name='student_list'),
    path('student/<int:student_id>/',               views.student_profile,  name='student_profile'),
    path('add/',                                    views.add_student,      name='add_student'),
    path('student/<int:student_id>/add-skill/',     views.add_skill,        name='add_skill'),
    path('student/<int:student_id>/delete/',        views.delete_student,   name='delete_student'),
    path('search/',                                 views.skill_search,     name='skill_search'),
    path('report/',                                 views.skill_report,     name='skill_report'),
]
