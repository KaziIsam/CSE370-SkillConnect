from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.contrib import messages
from django.db.models import Count, Q

from .models import (
    Student, Department, Skill, StudentSkill,
    UndergradStudent, GradStudent,
    Club, Event, ClubMembership, Participation
)


def raw_query(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        cols = [col[0] for col in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]


# ── Dashboard ─────────────────────────────────────────────────
def dashboard(request):
    total_students    = Student.objects.count()
    total_skills      = Skill.objects.count()
    total_assignments = StudentSkill.objects.count()
    total_departments = Department.objects.count()

    recent_students = (
        Student.objects.select_related('dept').order_by('-student_id')[:5]
    )

    top_skills = raw_query("""
        SELECT sk.skill_name, sk.category,
               COUNT(ss.student_id) AS student_count
        FROM Skill sk
        LEFT JOIN Student_Skill ss ON sk.skill_id = ss.skill_id
        GROUP BY sk.skill_id, sk.skill_name, sk.category
        ORDER BY student_count DESC LIMIT 5
    """)

    dept_counts = (
        Department.objects
        .annotate(student_count=Count('students'))
        .order_by('-student_count')
    )

    return render(request, 'students/dashboard.html', {
        'total_students':    total_students,
        'total_skills':      total_skills,
        'total_assignments': total_assignments,
        'total_departments': total_departments,
        'recent_students':   recent_students,
        'top_skills':        top_skills,
        'dept_counts':       dept_counts,
    })


# ── Student List ──────────────────────────────────────────────
def student_list(request):
    q           = request.GET.get('q', '').strip()
    dept_filter = request.GET.get('dept', '')
    type_filter = request.GET.get('type', '')
    year_filter = request.GET.get('year', '')

    qs = Student.objects.select_related('dept').order_by('name')

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q))
    if dept_filter:
        qs = qs.filter(dept__dept_code=dept_filter)
    if type_filter == 'Undergrad':
        qs = qs.filter(undergrad_profile__isnull=False)
    elif type_filter == 'Grad':
        qs = qs.filter(grad_profile__isnull=False)
    if year_filter:
        qs = qs.filter(enrollment_year=year_filter)

    qs = qs.annotate(skill_count=Count('skills'))

    return render(request, 'students/student_list.html', {
        'students':     qs,
        'departments':  Department.objects.all().order_by('dept_code'),
        'q':            q,
        'dept_filter':  dept_filter,
        'type_filter':  type_filter,
        'year_filter':  year_filter,
        'result_count': qs.count(),
    })


# ── Student Profile ───────────────────────────────────────────
def student_profile(request, student_id):
    student = get_object_or_404(
        Student.objects.select_related('dept'), pk=student_id
    )
    student_skills = (
        StudentSkill.objects.filter(student=student)
        .select_related('skill').order_by('skill__category')
    )

    undergrad_profile = None
    grad_profile      = None
    student_type      = 'Unknown'

    try:
        undergrad_profile = student.undergrad_profile
        student_type = 'Undergraduate'
    except UndergradStudent.DoesNotExist:
        pass

    try:
        grad_profile = student.grad_profile
        student_type = 'Graduate'
    except GradStudent.DoesNotExist:
        pass

    memberships    = ClubMembership.objects.filter(student=student).select_related('club')
    participations = (
        Participation.objects.filter(student=student)
        .select_related('event', 'event__club')
        .order_by('-event__event_date')
    )

    return render(request, 'students/student_profile.html', {
        'student':           student,
        'student_skills':    student_skills,
        'student_type':      student_type,
        'undergrad_profile': undergrad_profile,
        'grad_profile':      grad_profile,
        'memberships':       memberships,
        'participations':    participations,
        'total_skills':      student_skills.count(),
        'all_skills':        Skill.objects.all().order_by('skill_name'),
    })


# ── Skill Search ──────────────────────────────────────────────
def skill_search(request):
    all_skills  = Skill.objects.all().order_by('skill_name')
    departments = Department.objects.all().order_by('dept_code')
    results     = []
    searched    = False

    skill_name  = request.GET.get('skill', '').strip()
    proficiency = request.GET.get('proficiency', '').strip()
    dept_code   = request.GET.get('dept', '').strip()

    if skill_name or proficiency or dept_code:
        searched = True
        sql = """
            SELECT DISTINCT s.student_id, s.name, s.email,
                d.dept_name, d.dept_code,
                sk.skill_name, sk.category,
                ss.proficiency_level, ss.acquired_date
            FROM Student s
            JOIN Department d     ON s.dept_id    = d.dept_id
            JOIN Student_Skill ss ON s.student_id = ss.student_id
            JOIN Skill sk         ON ss.skill_id  = sk.skill_id
            WHERE 1=1
        """
        params = []
        if skill_name:
            sql += " AND sk.skill_name = %s"
            params.append(skill_name)
        if proficiency:
            sql += " AND ss.proficiency_level = %s"
            params.append(proficiency)
        if dept_code:
            sql += " AND d.dept_code = %s"
            params.append(dept_code)
        sql += " ORDER BY s.name"
        results = raw_query(sql, params)

    return render(request, 'students/skill_search.html', {
        'all_skills':           all_skills,
        'departments':          departments,
        'results':              results,
        'result_count':         len(results),
        'searched':             searched,
        'selected_skill':       skill_name,
        'selected_proficiency': proficiency,
        'selected_dept':        dept_code,
    })


# ── Skill Report ──────────────────────────────────────────────
def skill_report(request):
    report_data = raw_query("""
        SELECT sk.skill_id, sk.skill_name, sk.category,
            COUNT(ss.student_id)                        AS total_students,
            SUM(ss.proficiency_level = 'Beginner')      AS beginner_count,
            SUM(ss.proficiency_level = 'Intermediate')  AS intermediate_count,
            SUM(ss.proficiency_level = 'Advanced')      AS advanced_count
        FROM Skill sk
        LEFT JOIN Student_Skill ss ON sk.skill_id = ss.skill_id
        GROUP BY sk.skill_id, sk.skill_name, sk.category
        ORDER BY total_students DESC
    """)

    total_assignments = StudentSkill.objects.count()
    total_students    = Student.objects.count()
    avg_skills        = round(total_assignments / total_students, 1) if total_students else 0
    max_count         = max((r['total_students'] or 0 for r in report_data), default=1)

    return render(request, 'students/skill_report.html', {
        'report_data':       report_data,
        'total_assignments': total_assignments,
        'total_skills':      len(report_data),
        'avg_skills':        avg_skills,
        'max_count':         max_count,
    })


# ── Add Student ───────────────────────────────────────────────
def add_student(request):
    departments = Department.objects.all().order_by('dept_name')
    skills      = Skill.objects.all().order_by('skill_name')

    if request.method == 'POST':
        name            = request.POST.get('name', '').strip()
        email           = request.POST.get('email', '').strip()
        phone           = request.POST.get('phone', '').strip()
        enrollment_year = request.POST.get('enrollment_year')
        dept_id         = request.POST.get('dept_id')
        student_type    = request.POST.get('student_type', 'undergrad')

        errors = []
        if not name:            errors.append("Name is required.")
        if not email:           errors.append("Email is required.")
        if not dept_id:         errors.append("Department is required.")
        if not enrollment_year: errors.append("Enrollment year is required.")
        if not errors and Student.objects.filter(email=email).exists():
            errors.append("A student with this email already exists.")

        if errors:
            for err in errors:
                messages.error(request, err)
        else:
            student = Student.objects.create(
                name=name, email=email, phone=phone,
                enrollment_year=enrollment_year, dept_id=dept_id
            )
            if student_type == 'undergrad':
                UndergradStudent.objects.create(
                    student=student,
                    cgpa=request.POST.get('cgpa') or 0,
                    credit_completed=request.POST.get('credit_completed') or 0,
                    year_of_study=request.POST.get('year_of_study') or 1,
                )
            else:
                GradStudent.objects.create(
                    student=student,
                    thesis_topic=request.POST.get('thesis_topic', ''),
                    supervisor=request.POST.get('supervisor', ''),
                    research_area=request.POST.get('research_area', ''),
                )

            skill_ids     = request.POST.getlist('skill_ids')
            proficiencies = request.POST.getlist('proficiencies')
            dates         = request.POST.getlist('acquired_dates')
            for i, skill_id in enumerate(skill_ids):
                if skill_id:
                    StudentSkill.objects.get_or_create(
                        student_id=student.student_id,
                        skill_id=skill_id,
                        defaults={
                            'proficiency_level': proficiencies[i] if i < len(proficiencies) else 'Beginner',
                            'acquired_date':     dates[i] if i < len(dates) and dates[i] else None,
                        }
                    )

            messages.success(request, f"Student '{name}' registered successfully!")
            return redirect('student_profile', student_id=student.student_id)

    return render(request, 'students/add_student.html', {
        'departments': departments,
        'skills':      skills,
    })


# ── Add Skill to Student ──────────────────────────────────────
def add_skill(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        skill_id          = request.POST.get('skill_id')
        proficiency_level = request.POST.get('proficiency_level')
        acquired_date     = request.POST.get('acquired_date') or None
        if not skill_id or not proficiency_level:
            messages.error(request, "Please select both a skill and proficiency level.")
        else:
            obj, created = StudentSkill.objects.get_or_create(
                student_id=student_id, skill_id=skill_id,
                defaults={'proficiency_level': proficiency_level, 'acquired_date': acquired_date}
            )
            if created:
                messages.success(request, "Skill added!")
            else:
                messages.warning(request, "Student already has this skill.")
    return redirect('student_profile', student_id=student_id)


# ── Delete Student ────────────────────────────────────────────
def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f"Student '{name}' deleted.")
        return redirect('student_list')
    return render(request, 'students/confirm_delete.html', {'student': student})
