from django.db import models


class Department(models.Model):
    dept_id   = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    dept_code = models.CharField(max_length=10, unique=True)

    class Meta:
        managed  = False
        db_table = 'Department'

    def __str__(self):
        return f"{self.dept_code} — {self.dept_name}"


class Student(models.Model):
    student_id      = models.AutoField(primary_key=True)
    name            = models.CharField(max_length=100)
    email           = models.CharField(max_length=100, unique=True)
    phone           = models.CharField(max_length=15, blank=True, null=True)
    enrollment_year = models.IntegerField()
    dept            = models.ForeignKey(
                          Department,
                          on_delete=models.PROTECT,
                          db_column='dept_id',
                          related_name='students'
                      )

    class Meta:
        managed  = False
        db_table = 'Student'

    def __str__(self):
        return self.name

    def get_initials(self):
        parts = self.name.strip().split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return self.name[:2].upper()


class Skill(models.Model):
    skill_id   = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100, unique=True)
    category   = models.CharField(max_length=50)

    class Meta:
        managed  = False
        db_table = 'Skill'

    def __str__(self):
        return self.skill_name


class SkillTools(models.Model):
    skill     = models.ForeignKey(
                    Skill,
                    on_delete=models.CASCADE,
                    db_column='skill_id',
                    related_name='tools'
                )
    tool_name = models.CharField(max_length=100)

    class Meta:
        managed         = False
        db_table        = 'Skill_Tools'
        unique_together = (('skill', 'tool_name'),)


class StudentSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner',     'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced',     'Advanced'),
    ]
    student           = models.ForeignKey(
                            Student,
                            on_delete=models.CASCADE,
                            db_column='student_id',
                            related_name='skills'
                        )
    skill             = models.ForeignKey(
                            Skill,
                            on_delete=models.CASCADE,
                            db_column='skill_id',
                            related_name='student_skills'
                        )
    proficiency_level = models.CharField(max_length=12, choices=PROFICIENCY_CHOICES)
    acquired_date     = models.DateField(null=True, blank=True)

    class Meta:
        managed         = False
        db_table        = 'Student_Skill'
        unique_together = (('student', 'skill'),)

    def __str__(self):
        return f"{self.student.name} — {self.skill.skill_name}"


class Club(models.Model):
    club_id       = models.AutoField(primary_key=True)
    club_name     = models.CharField(max_length=100, unique=True)
    description   = models.TextField(blank=True, null=True)
    founding_year = models.IntegerField(null=True, blank=True)

    class Meta:
        managed  = False
        db_table = 'Club'

    def __str__(self):
        return self.club_name


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


class Participation(models.Model):
    STATUS_CHOICES = [
        ('Registered', 'Registered'),
        ('Attended',   'Attended'),
        ('Cancelled',  'Cancelled'),
    ]
    student           = models.ForeignKey(
                            Student,
                            on_delete=models.CASCADE,
                            db_column='student_id',
                            related_name='participations'
                        )
    event             = models.ForeignKey(
                            Event,
                            on_delete=models.CASCADE,
                            db_column='event_id',
                            related_name='participants'
                        )
    registration_date = models.DateField(null=True, blank=True)
    status            = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Registered')

    class Meta:
        managed         = False
        db_table        = 'Participation'
        unique_together = (('student', 'event'),)


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
    joined_date = models.DateField(null=True, blank=True)
    role        = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    class Meta:
        managed         = False
        db_table        = 'ClubMembership'
        unique_together = (('student', 'club'),)


class UndergradStudent(models.Model):
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
