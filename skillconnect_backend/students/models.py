"""
students/models.py
==================
WHY MODELS?
  A model is a Python class that represents a database table.
  Each attribute = one column.
  Django uses these classes to talk to MySQL.

WHY managed = False?
  We ALREADY created our tables in MySQL manually (Step 3).
  If managed=True, Django would try to recreate them — that
  would cause errors. managed=False tells Django:
  "The table exists. Don't touch it. Just READ and WRITE."

WHY db_table = 'TableName'?
  By default Django names tables like 'students_student'.
  But ours are named 'Student', 'Skill' etc.
  db_table tells Django the exact table name to use.
"""

from django.db import models


# ─────────────────────────────────────────────────────────
# Department
# ─────────────────────────────────────────────────────────
class Department(models.Model):
    dept_id   = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    dept_code = models.CharField(max_length=10, unique=True)

    class Meta:
        managed  = False        # table already exists in MySQL
        db_table = 'Department' # exact name of the MySQL table

    def __str__(self):
        # __str__ controls what shows in Django admin panel
        # and when you print a Department object
        return f"{self.dept_code} — {self.dept_name}"


# ─────────────────────────────────────────────────────────
# Student
# ─────────────────────────────────────────────────────────
class Student(models.Model):
    student_id      = models.AutoField(primary_key=True)
    name            = models.CharField(max_length=100)
    email           = models.CharField(max_length=100, unique=True)
    phone           = models.CharField(max_length=15, blank=True, null=True)
    enrollment_year = models.IntegerField()

    # ForeignKey = the FK relationship to Department
    # on_delete=RESTRICT → mirrors our SQL: ON DELETE RESTRICT
    # db_column='dept_id' → the actual column name in MySQL
    dept = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        db_column='dept_id',
        related_name='students'
    )

    class Meta:
        managed  = False
        db_table = 'Student'

    def __str__(self):
        return f"{self.name} ({self.dept.dept_code})"

    def get_initials(self):
        """Returns initials like 'AH' for 'Arif Hossain' — used in avatar"""
        parts = self.name.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return self.name[:2].upper()


# ─────────────────────────────────────────────────────────
# Skill
# ─────────────────────────────────────────────────────────
class Skill(models.Model):
    skill_id   = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100, unique=True)
    category   = models.CharField(max_length=50)

    class Meta:
        managed  = False
        db_table = 'Skill'

    def __str__(self):
        return f"{self.skill_name} ({self.category})"


# ─────────────────────────────────────────────────────────
# Skill_Tools (multi-valued attribute)
# ─────────────────────────────────────────────────────────
class SkillTools(models.Model):
    skill     = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        db_column='skill_id',
        related_name='tools'
    )
    tool_name = models.CharField(max_length=100)

    class Meta:
        managed  = False
        db_table = 'Skill_Tools'
        # Composite PK: (skill_id, tool_name)
        unique_together = (('skill', 'tool_name'),)

    def __str__(self):
        return f"{self.skill.skill_name} → {self.tool_name}"


# ─────────────────────────────────────────────────────────
# Student_Skill (junction table)
# ─────────────────────────────────────────────────────────
class StudentSkill(models.Model):

    PROFICIENCY_CHOICES = [
        ('Beginner',     'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced',     'Advanced'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        db_column='student_id',
        related_name='skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        db_column='skill_id',
        related_name='student_skills'
    )
    proficiency_level = models.CharField(
        max_length=12,
        choices=PROFICIENCY_CHOICES
    )
    acquired_date = models.DateField(null=True, blank=True)

    class Meta:
        managed      = False
        db_table     = 'Student_Skill'
        # Composite PK — same student cannot have same skill twice
        unique_together = (('student', 'skill'),)

    def __str__(self):
        return f"{self.student.name} — {self.skill.skill_name} ({self.proficiency_level})"


# ─────────────────────────────────────────────────────────
# Club (for participation context — Member 2's table)
# We still need to READ this for cross-module queries
# ─────────────────────────────────────────────────────────
class Club(models.Model):
    club_id      = models.AutoField(primary_key=True)
    club_name    = models.CharField(max_length=100, unique=True)
    description  = models.TextField(blank=True, null=True)
    founding_year = models.IntegerField(null=True, blank=True)

    class Meta:
        managed  = False
        db_table = 'Club'

    def __str__(self):
        return self.club_name


# ─────────────────────────────────────────────────────────
# Event
# ─────────────────────────────────────────────────────────
class Event(models.Model):
    event_id         = models.AutoField(primary_key=True)
    event_name       = models.CharField(max_length=100)
    event_date       = models.DateField()
    location         = models.CharField(max_length=100, blank=True, null=True)
    max_participants = models.IntegerField(default=100)
    club             = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        db_column='club_id',
        related_name='events'
    )

    class Meta:
        managed  = False
        db_table = 'Event'

    def __str__(self):
        return self.event_name


# ─────────────────────────────────────────────────────────
# Participation (junction — Member 3's table)
# ─────────────────────────────────────────────────────────
class Participation(models.Model):

    STATUS_CHOICES = [
        ('Registered', 'Registered'),
        ('Attended',   'Attended'),
        ('Cancelled',  'Cancelled'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        db_column='student_id',
        related_name='participations'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        db_column='event_id',
        related_name='participants'
    )
    registration_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Registered'
    )

    class Meta:
        managed      = False
        db_table     = 'Participation'
        unique_together = (('student', 'event'),)

    def __str__(self):
        return f"{self.student.name} → {self.event.event_name}"


# ─────────────────────────────────────────────────────────
# ClubMembership (associative entity)
# ─────────────────────────────────────────────────────────
class ClubMembership(models.Model):

    ROLE_CHOICES = [
        ('Member',         'Member'),
        ('Coordinator',    'Coordinator'),
        ('President',      'President'),
        ('Vice President', 'Vice President'),
        ('Secretary',      'Secretary'),
    ]

    student     = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        db_column='student_id',
        related_name='club_memberships'
    )
    club        = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        db_column='club_id',
        related_name='members'
    )
    joined_date = models.DateField()
    role        = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    class Meta:
        managed      = False
        db_table     = 'club_membership'  # ← lowercase as created in MySQL
        unique_together = (('student', 'club'),)

    def __str__(self):
        return f"{self.student.name} — {self.club.club_name} ({self.role})"


# ─────────────────────────────────────────────────────────
# UndergradStudent (ISA specialization subtype)
# ─────────────────────────────────────────────────────────
class UndergradStudent(models.Model):
    # student_id is BOTH PK and FK — one-to-one with Student
    student          = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='student_id',
        related_name='undergrad_profile'
    )
    cgpa             = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    credit_completed = models.IntegerField(default=0)
    year_of_study    = models.IntegerField()

    class Meta:
        managed  = False
        db_table = 'UndergradStudent'

    def __str__(self):
        return f"UG: {self.student.name} (CGPA: {self.cgpa})"


# ─────────────────────────────────────────────────────────
# GradStudent (ISA specialization subtype)
# ─────────────────────────────────────────────────────────
class GradStudent(models.Model):
    student       = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='student_id',
        related_name='grad_profile'
    )
    thesis_topic  = models.CharField(max_length=200, blank=True, null=True)
    supervisor    = models.CharField(max_length=100)
    research_area = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'GradStudent'

    def __str__(self):
        return f"Grad: {self.student.name} — {self.research_area}"