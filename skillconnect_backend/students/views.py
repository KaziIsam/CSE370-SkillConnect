"""
students/views.py
=================
WHY VIEWS?
  A view is a Python function that:
  1. Receives a browser request
  2. Talks to the database via models
  3. Sends data to a template (HTML page)
  4. Returns the rendered HTML to the browser

  Request → View → Model (DB) → Template → Response

HOW IT WORKS:
  URL:  /students/search/?skill=Python&proficiency=Advanced
  Django runs skill_search(request)
  → reads request.GET.get('skill') = 'Python'
  → queries DB
  → sends results to skill_search.html
  → browser shows the page with real data
"""

from django.shortcuts     import render, get_object_or_404, redirect
from django.db            import connection
from django.contrib       import messages
from django.db.models     import Count, Q

from .models import (
    Student, Department, Skill, StudentSkill,
    UndergradStudent, GradStudent,
    Club, Event, ClubMembership, Participation
)
from .forms import StudentForm, StudentSkillForm


# ═══════════════════════════════════════════════════════════
# HELPER — run raw SQL and return list of dicts
# ═══════════════════════════════════════════════════════════
def raw_query(sql, params=None):
    """
    Execute raw SQL and return results as a list of dicts.
    WHY raw SQL sometimes?
      For complex multi-JOIN analytics queries it is
      cleaner and easier to debug than ORM syntax.
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        cols    = [col[0] for col in cursor.description]
        results = [dict(zip(cols, row)) for row in cursor.fetchall()]
    return results


# ═══════════════════════════════════════════════════════════
# VIEW 1: DASHBOARD
# URL: /students/  or  /
# ═══════════════════════════════════════════════════════════
def dashboard(request):
    """
    The homepage. Shows summary statistics and quick tables.

    HOW COUNT works with Django ORM:
      Student.objects.count() → SELECT COUNT(*) FROM Student
    """
    # — Stat cards —
    total_students   = Student.objects.count()
    total_skills     = Skill.objects.count()
    total_assignments = StudentSkill.objects.count()
    total_departments = Department.objects.count()

    # — Recent 5 students (ordered by newest first) —
    recent_students = (
        Student.objects
        .select_related('dept')           # JOIN with Department in one query
        .order_by('-student_id')          # newest first
        [:5]                              # LIMIT 5
    )

    # — Top 5 skills by student count (raw SQL for GROUP BY) —
    top_skills = raw_query("""
        SELECT
            sk.skill_name,
            sk.category,
            COUNT(ss.student_id) AS student_count
        FROM Skill sk
        LEFT JOIN Student_Skill ss ON sk.skill_id = ss.skill_id
        GROUP BY sk.skill_id, sk.skill_name, sk.category
        ORDER BY student_count DESC
        LIMIT 5
    """)

    # — Dept breakdown —
    dept_counts = (
        Department.objects
        .annotate(student_count=Count('students'))
        .order_by('-student_count')
    )

    context = {
        'total_students':    total_students,
        'total_skills':      total_skills,
        'total_assignments': total_assignments,
        'total_departments': total_departments,
        'recent_students':   recent_students,
        'top_skills':        top_skills,
        'dept_counts':       dept_counts,
    }
    return render(request, 'students/dashboard.html', context)
    # render() = load template + inject context data → return HTML


# ═══════════════════════════════════════════════════════════
# VIEW 2: STUDENT LIST
# URL: /students/list/
# ═══════════════════════════════════════════════════════════
def student_list(request):
    """
    Shows all students with search + filter.

    HOW GET PARAMETERS WORK:
      URL: /students/list/?dept=CSE&type=Undergrad
      request.GET.get('dept') → 'CSE'
      request.GET.get('type') → 'Undergrad'
      request.GET.get('q')    → None (not in URL)

    HOW FILTERING WORKS:
      We start with ALL students, then chain .filter()
      calls based on what the user selected.
      Each .filter() adds a WHERE clause to the SQL.
    """
    # Read URL parameters
    q           = request.GET.get('q', '').strip()
    dept_filter = request.GET.get('dept', '')
    type_filter = request.GET.get('type', '')
    year_filter = request.GET.get('year', '')

    # Start with all students + JOIN department
    qs = Student.objects.select_related('dept').order_by('name')

    # Apply search filter (name OR email)
    if q:
        qs = qs.filter(
            Q(name__icontains=q) | Q(email__icontains=q)
            # Q objects allow OR conditions
            # icontains = case-insensitive LIKE %q%
        )

    # Apply department filter
    if dept_filter:
        qs = qs.filter(dept__dept_code=dept_filter)
        # dept__dept_code = follow FK to Department, filter by dept_code

    # Apply type filter (Undergrad / Grad)
    if type_filter == 'Undergrad':
        # Students who HAVE an UndergradStudent row
        qs = qs.filter(undergrad_profile__isnull=False)
    elif type_filter == 'Grad':
        qs = qs.filter(grad_profile__isnull=False)

    # Apply year filter
    if year_filter:
        qs = qs.filter(enrollment_year=year_filter)

    # Annotate each student with their skill count
    qs = qs.annotate(skill_count=Count('skills'))

    # Get all departments for the filter dropdown
    departments = Department.objects.all().order_by('dept_code')

    context = {
        'students':    qs,
        'departments': departments,
        'q':           q,
        'dept_filter': dept_filter,
        'type_filter': type_filter,
        'year_filter': year_filter,
        'result_count': qs.count(),
    }
    return render(request, 'students/student_list.html', context)


# ═══════════════════════════════════════════════════════════
# VIEW 3: STUDENT PROFILE
# URL: /students/<student_id>/
# ═══════════════════════════════════════════════════════════
def student_profile(request, student_id):
    """
    Shows one student's full profile — all skills, subtype info.

    get_object_or_404:
      Tries to find Student with that ID.
      If not found → shows 404 page automatically.
      Much cleaner than try/except.
    """
    student = get_object_or_404(
        Student.objects.select_related('dept'),
        pk=student_id
    )

    # Get all skills for this student
    student_skills = (
        StudentSkill.objects
        .filter(student=student)
        .select_related('skill')
        .order_by('skill__category', 'skill__skill_name')
    )

    # Check if Undergrad or Grad (ISA specialization)
    undergrad_profile = None
    grad_profile      = None
    student_type      = 'Unknown'

    try:
        undergrad_profile = student.undergrad_profile
        student_type      = 'Undergraduate'
    except UndergradStudent.DoesNotExist:
        pass

    try:
        grad_profile  = student.grad_profile
        student_type  = 'Graduate'
    except GradStudent.DoesNotExist:
        pass

    # Get club memberships
    memberships = (
        ClubMembership.objects
        .filter(student=student)
        .select_related('club')
    )

    # Get event participations
    participations = (
        Participation.objects
        .filter(student=student)
        .select_related('event', 'event__club')
        .order_by('-event__event_date')
    )

    context = {
        'student':           student,
        'student_skills':    student_skills,
        'student_type':      student_type,
        'undergrad_profile': undergrad_profile,
        'grad_profile':      grad_profile,
        'memberships':       memberships,
        'participations':    participations,
        'total_skills':      student_skills.count(),
    }
    return render(request, 'students/student_profile.html', context)


# ═══════════════════════════════════════════════════════════
# VIEW 4: SKILL SEARCH
# URL: /students/search/
# ═══════════════════════════════════════════════════════════
def skill_search(request):
    """
    Search students by skill + proficiency + department.

    WHY raw SQL here instead of ORM?
      This query touches 4 tables with multiple JOINs.
      Raw SQL is easier to read and debug for complex queries.
      The ORM would work too, but the SQL is clearer.
    """
    all_skills   = Skill.objects.all().order_by('skill_name')
    departments  = Department.objects.all().order_by('dept_code')
    results      = []
    searched     = False

    # Read filters from URL
    skill_name  = request.GET.get('skill', '').strip()
    proficiency = request.GET.get('proficiency', '').strip()
    dept_code   = request.GET.get('dept', '').strip()

    if skill_name or proficiency or dept_code:
        searched = True

        # Build the SQL dynamically
        sql = """
            SELECT DISTINCT
                s.student_id,
                s.name,
                s.email,
                d.dept_name,
                d.dept_code,
                sk.skill_name,
                sk.category,
                ss.proficiency_level,
                ss.acquired_date
            FROM Student s
            JOIN Department d     ON s.dept_id    = d.dept_id
            JOIN Student_Skill ss ON s.student_id = ss.student_id
            JOIN Skill sk         ON ss.skill_id  = sk.skill_id
            WHERE 1=1
        """
        # WHY WHERE 1=1?
        # It is always true. This lets us safely add AND clauses
        # without worrying about whether to put WHERE or AND first.
        params = []

        if skill_name:
            sql += " AND sk.skill_name = %s"
            params.append(skill_name)
            # %s is a safe placeholder — prevents SQL injection

        if proficiency:
            sql += " AND ss.proficiency_level = %s"
            params.append(proficiency)

        if dept_code:
            sql += " AND d.dept_code = %s"
            params.append(dept_code)

        sql += " ORDER BY s.name, sk.skill_name"

        results = raw_query(sql, params)

    context = {
        'all_skills':           all_skills,
        'departments':          departments,
        'results':              results,
        'result_count':         len(results),
        'searched':             searched,
        'selected_skill':       skill_name,
        'selected_proficiency': proficiency,
        'selected_dept':        dept_code,
    }
    return render(request, 'students/skill_search.html', context)


# ═══════════════════════════════════════════════════════════
# VIEW 5: SKILL DISTRIBUTION REPORT
# URL: /students/report/
# ═══════════════════════════════════════════════════════════
def skill_report(request):
    """
    Analytics report: how many students per skill,
    broken down by proficiency level.

    WHY SUM(condition) in MySQL?
      In MySQL, TRUE = 1 and FALSE = 0.
      SUM(ss.proficiency_level = 'Advanced') counts
      only the rows where that condition is true.
      This is the standard MySQL technique for pivot counting.
    """
    report_data = raw_query("""
        SELECT
            sk.skill_id,
            sk.skill_name,
            sk.category,
            COUNT(ss.student_id)                            AS total_students,
            SUM(ss.proficiency_level = 'Beginner')         AS beginner_count,
            SUM(ss.proficiency_level = 'Intermediate')     AS intermediate_count,
            SUM(ss.proficiency_level = 'Advanced')         AS advanced_count
        FROM Skill sk
        LEFT JOIN Student_Skill ss ON sk.skill_id = ss.skill_id
        GROUP BY sk.skill_id, sk.skill_name, sk.category
        ORDER BY total_students DESC, sk.skill_name
    """)

    # Summary stats
    total_assignments = StudentSkill.objects.count()
    total_students    = Student.objects.count()
    avg_skills        = round(total_assignments / total_students, 1) if total_students else 0

    # Find max for percentage calculation in template
    max_count = max((r['total_students'] for r in report_data), default=1)

    context = {
        'report_data':      report_data,
        'total_assignments': total_assignments,
        'total_skills':      len(report_data),
        'avg_skills':        avg_skills,
        'max_count':         max_count,
    }
    return render(request, 'students/skill_report.html', context)


# ═══════════════════════════════════════════════════════════
# VIEW 6: ADD STUDENT
# URL: /students/add/
# ═══════════════════════════════════════════════════════════
def add_student(request):
    """
    Register a new student.

    HOW FORMS WORK IN DJANGO:
      GET request  → show empty form
      POST request → validate and save data

    request.method:
      'GET'  → user just opened the page
      'POST' → user clicked the Submit button

    form.is_valid():
      Runs all validation rules defined in forms.py
      If valid → save to DB
      If invalid → show form again with error messages
    """
    departments = Department.objects.all().order_by('dept_name')
    skills      = Skill.objects.all().order_by('skill_name')

    if request.method == 'POST':
        # Read all form data from the POST request
        name            = request.POST.get('name', '').strip()
        email           = request.POST.get('email', '').strip()
        phone           = request.POST.get('phone', '').strip()
        enrollment_year = request.POST.get('enrollment_year')
        dept_id         = request.POST.get('dept_id')
        student_type    = request.POST.get('student_type', 'undergrad')

        # Basic validation
        errors = []
        if not name:
            errors.append("Name is required.")
        if not email:
            errors.append("Email is required.")
        elif Student.objects.filter(email=email).exists():
            errors.append("A student with this email already exists.")
        if not dept_id:
            errors.append("Department is required.")
        if not enrollment_year:
            errors.append("Enrollment year is required.")

        if errors:
            for err in errors:
                messages.error(request, err)
        else:
            # Save Student
            student = Student.objects.create(
                name            = name,
                email           = email,
                phone           = phone,
                enrollment_year = enrollment_year,
                dept_id         = dept_id
            )

            # Save subtype based on ISA selection
            if student_type == 'undergrad':
                UndergradStudent.objects.create(
                    student          = student,
                    cgpa             = request.POST.get('cgpa') or 0,
                    credit_completed = request.POST.get('credit_completed') or 0,
                    year_of_study    = request.POST.get('year_of_study') or 1,
                )
            else:
                GradStudent.objects.create(
                    student       = student,
                    thesis_topic  = request.POST.get('thesis_topic', ''),
                    supervisor    = request.POST.get('supervisor', ''),
                    research_area = request.POST.get('research_area', ''),
                )

            # Save selected skills
            skill_ids    = request.POST.getlist('skill_ids')
            proficiencies = request.POST.getlist('proficiencies')
            dates         = request.POST.getlist('acquired_dates')

            for i, skill_id in enumerate(skill_ids):
                if skill_id:
                    StudentSkill.objects.get_or_create(
                        student   = student,
                        skill_id  = skill_id,
                        defaults  = {
                            'proficiency_level': proficiencies[i] if i < len(proficiencies) else 'Beginner',
                            'acquired_date':     dates[i] if i < len(dates) and dates[i] else None,
                        }
                    )

            messages.success(request, f"Student '{name}' registered successfully!")
            return redirect('student_profile', student_id=student.student_id)
            # redirect() sends user to the profile page after saving

    context = {
        'departments': departments,
        'skills':      skills,
    }
    return render(request, 'students/add_student.html', context)


# ═══════════════════════════════════════════════════════════
# VIEW 7: ADD SKILL TO EXISTING STUDENT
# URL: /students/<student_id>/add-skill/
# ═══════════════════════════════════════════════════════════
def add_skill(request, student_id):
    """
    Add a skill to an existing student's profile.
    This handles the POST from the profile page skill form.
    """
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        skill_id          = request.POST.get('skill_id')
        proficiency_level = request.POST.get('proficiency_level')
        acquired_date     = request.POST.get('acquired_date') or None

        if not skill_id or not proficiency_level:
            messages.error(request, "Please select both a skill and proficiency level.")
        else:
            # get_or_create: insert if not exists, skip if already exists
            obj, created = StudentSkill.objects.get_or_create(
                student_id = student_id,
                skill_id   = skill_id,
                defaults   = {
                    'proficiency_level': proficiency_level,
                    'acquired_date':     acquired_date,
                }
            )
            if created:
                messages.success(request, "Skill added successfully!")
            else:
                messages.warning(request, "This student already has that skill.")

    return redirect('student_profile', student_id=student_id)


# ═══════════════════════════════════════════════════════════
# VIEW 8: DELETE STUDENT
# URL: /students/<student_id>/delete/
# ═══════════════════════════════════════════════════════════
def delete_student(request, student_id):
    """
    Delete a student and all their related records.
    ON DELETE CASCADE in MySQL handles the related records automatically.
    Only allow POST (not GET) for safety.
    """
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        name = student.name
        student.delete()
        # Because of ON DELETE CASCADE in MySQL,
        # Student_Skill, Participation, ClubMembership,
        # UndergradStudent, GradStudent rows are all deleted too.
        messages.success(request, f"Student '{name}' deleted successfully.")
        return redirect('student_list')

    return render(request, 'students/confirm_delete.html', {'student': student})