# 🎓 BRAC SkillConnect
### Student Skill & Club Event Management System
> CSE370 — Database Systems | BRAC University

---

## 📌 Project Overview

BRAC SkillConnect is a full-stack web application designed to manage
student skills, club activities, and event participation within
BRAC University. Built as part of CSE370 (Database Systems) course,
focusing on relational database concepts including normalization,
EER design, and SQL queries.


---

## 🏗️ Project Modules

### 👤 Part-01 — Student & Skill Management
- Student registration and profile management
- Add and manage skills with proficiency levels (Beginner / Intermediate / Advanced)
- Search students by skill
- Filter by skill, proficiency level, and department
- Skill distribution analytics report
- ISA Specialization — Undergraduate and Graduate students

### 🏢 Part-02 — Club & Event Management
- Club information management
- Event creation and management
- Event participation count report

### 📊 Part-03 — Participation & Analytics
- Student event participation tracking
- Most active student report
- Most popular club report

---

## 🗄️ Database Design

### Entities
| Entity | Description |
|--------|------------|
| Department | Academic departments |
| Student | University students (central entity) |
| Skill | Available skills |
| Student_Skill | Junction — student skill assignments |
| Club | University clubs |
| Event | Club-organized events |
| Participation | Junction — student event attendance |
| ClubMembership | Junction — student club memberships |
| UndergradStudent | ISA subtype of Student |
| GradStudent | ISA subtype of Student |

### Relationships
Student  → Department   (Many-to-One | Total participation on Student)
Student  ↔ Skill        (Many-to-Many via Student_Skill)
Club     → Event        (One-to-Many)
Student  ↔ Event        (Many-to-Many via Participation)
Student  ↔ Club         (Many-to-Many via ClubMembership)

### Key Design Decisions
- **ISA Specialization** — Student split into UndergradStudent and GradStudent (Disjoint, Total)
- **Composite Primary Keys** — All junction tables use composite PKs to prevent duplicates
- **3NF Normalization** — All tables satisfy Third Normal Form
- **Multi-valued attribute** — skill_tools stored in separate Skill_Tools table
- **Derived attribute** — total_skill computed via SQL COUNT, not stored as column

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Django 4.2 (Python) |
| Database | MySQL 8.0 |
| Tools | MySQL Workbench, VS Code, Git, GitHub |

---

## 📁 Project Structure
CSE370_project/
├── database/
│   ├── 01_sample_table.sql       # CREATE TABLE queries
│   ├── 02_sample_data.sql        # INSERT sample data
│   └── 03_sample_queries.sql     # SELECT queries for reports
│
├── skillconnect_backend/         # Django backend
│   ├── skillconnect/
│   │   ├── settings.py           # Django + MySQL config
│   │   ├── urls.py               # Main URL router
│   │   └── init.py           # pymysql patch
│   ├── students/
│   │   ├── models.py             # Database models
│   │   ├── views.py              # Page logic
│   │   ├── urls.py               # URL routes
│   │   ├── admin.py              # Admin panel
│   │   └── templates/students/   # HTML templates
│   └── manage.py
│
└── skillconnect_frontend/        # Static HTML prototype
├── dashboard.html
├── student_list.html
├── skill_search.html
├── skill_report.html
└── add_student.html

---

## 🚀 How to Run

### Prerequisites
- Python 3.x with Anaconda
- MySQL 8.0
- MySQL Workbench

### Step 1 — Setup Database
```sql
CREATE DATABASE skillconnect;
```
Then run `01_sample_table.sql` → then `02_sample_data.sql` in MySQL Workbench.

### Step 2 — Install Dependencies
```bash
pip install django pymysql
```

### Step 3 — Configure Database
Open `skillconnect_backend/skillconnect/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'skillconnect',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### Step 4 — Run Server
```bash
cd skillconnect_backend
python manage.py runserver
```

### Step 5 — Open Browser
http://127.0.0.1:8000/students/

---

## 📊 Key SQL Queries

### Skill Distribution Report
```sql
SELECT sk.skill_name, sk.category,
       COUNT(ss.student_id)                       AS total_students,
       SUM(ss.proficiency_level = 'Beginner')     AS beginner_count,
       SUM(ss.proficiency_level = 'Intermediate') AS intermediate_count,
       SUM(ss.proficiency_level = 'Advanced')     AS advanced_count
FROM Skill sk
LEFT JOIN Student_Skill ss ON sk.skill_id = ss.skill_id
GROUP BY sk.skill_id
ORDER BY total_students DESC;
```

### Search Students by Skill
```sql
SELECT s.name, s.email, d.dept_name,
       sk.skill_name, ss.proficiency_level
FROM Student s
JOIN Department d     ON s.dept_id    = d.dept_id
JOIN Student_Skill ss ON s.student_id = ss.student_id
JOIN Skill sk         ON ss.skill_id  = sk.skill_id
WHERE sk.skill_name = 'Python'
ORDER BY ss.proficiency_level;
```

### Most Active Student
```sql
SELECT s.name, d.dept_name,
       COUNT(p.event_id) AS events_attended
FROM Student s
JOIN Department d         ON s.dept_id    = d.dept_id
LEFT JOIN Participation p ON s.student_id = p.student_id
GROUP BY s.student_id
ORDER BY events_attended DESC
LIMIT 5;
```

---

## 🔗 Application Pages

| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/students/` | Overview with stats |
| All Students | `/students/list/` | Full list with filters |
| Student Profile | `/students/student/<id>/` | Individual profile |
| Add Student | `/students/add/` | Register new student |
| Search by Skill | `/students/search/` | Find students by skill |
| Skill Report | `/students/report/` | Analytics dashboard |

---

## 🎓 Course Information

- **Course**: CSE370 — Database Systems
- **University**: BRAC University
