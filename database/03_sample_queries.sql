-- ============================================================
-- QUERY 1: View ALL students with their department
-- Tables used: Student + Department
-- ============================================================
SELECT
    s.student_id,
    s.name,
    s.email,
    s.phone,
    s.enrollment_year,
    d.dept_name
FROM Student s
JOIN Department d ON s.dept_id = d.dept_id
ORDER BY s.name ASC;

-- WHY JOIN here?
-- dept_name lives in Department table, not in Student.
-- We bridge them using the matching dept_id column.
-- ORDER BY name shows results alphabetically.



-- ============================================================
-- QUERY 2: Search students by SKILL NAME (core feature)
-- Tables used: Student + Student_Skill + Skill + Department
-- ============================================================
SELECT
    s.student_id,
    s.name,
    s.email,
    d.dept_name,
    sk.skill_name,
    ss.proficiency_level,
    ss.acquired_date
FROM Student s
JOIN Department d      ON s.dept_id   = d.dept_id
JOIN Student_Skill ss  ON s.student_id = ss.student_id
JOIN Skill sk          ON ss.skill_id  = sk.skill_id
WHERE sk.skill_name = 'Python'   -- ← change this to any skill
ORDER BY ss.proficiency_level;

-- WHY 3 JOINs?
-- Student → Student_Skill → Skill
-- Each JOIN adds one more table's columns to our result.
-- We filter AFTER joining using WHERE.


-- ============================================================
-- QUERY 3: Filter by SKILL + PROFICIENCY LEVEL
-- ============================================================
SELECT
    s.name,
    s.email,
    d.dept_name,
    sk.skill_name,
    ss.proficiency_level
FROM Student s
JOIN Department d      ON s.dept_id    = d.dept_id
JOIN Student_Skill ss  ON s.student_id = ss.student_id
JOIN Skill sk          ON ss.skill_id  = sk.skill_id
WHERE sk.skill_name       = 'Python'
  AND ss.proficiency_level = 'Advanced';

-- WHY AND?
-- AND chains two conditions. BOTH must be true.
-- This returns only Advanced Python students.


-- ============================================================
-- QUERY 4: Filter students by DEPARTMENT
-- ============================================================
SELECT
    s.name,
    s.email,
    d.dept_name,
    sk.skill_name,
    ss.proficiency_level
FROM Student s
JOIN Department d      ON s.dept_id    = d.dept_id
JOIN Student_Skill ss  ON s.student_id = ss.student_id
JOIN Skill sk          ON ss.skill_id  = sk.skill_id
WHERE d.dept_code = 'CSE'
ORDER BY s.name;



-- ============================================================
-- QUERY 5: Full STUDENT PROFILE VIEW
-- Shows student info + ALL their skills
-- ============================================================
SELECT
    s.student_id,
    s.name,
    s.email,
    s.enrollment_year,
    d.dept_name,
    sk.skill_name,
    sk.category,
    ss.proficiency_level,
    ss.acquired_date
FROM Student s
JOIN Department d      ON s.dept_id    = d.dept_id
JOIN Student_Skill ss  ON s.student_id = ss.student_id
JOIN Skill sk          ON ss.skill_id  = sk.skill_id
WHERE s.student_id = 1   -- ← change to any student_id
ORDER BY sk.category;


-- ============================================================
-- QUERY 6: SKILL DISTRIBUTION REPORT
-- How many students per skill + breakdown by level
-- This is your analytics report — important for viva!
-- ============================================================
SELECT
    sk.skill_name,
    sk.category,
    COUNT(ss.student_id)                              AS total_students,
    SUM(ss.proficiency_level = 'Beginner')            AS beginner_count,
    SUM(ss.proficiency_level = 'Intermediate')        AS intermediate_count,
    SUM(ss.proficiency_level = 'Advanced')            AS advanced_count
FROM Skill sk
LEFT JOIN Student_Skill ss ON sk.skill_id = ss.skill_id
GROUP BY sk.skill_id, sk.skill_name, sk.category
ORDER BY total_students DESC;

-- WHY LEFT JOIN here instead of JOIN?
-- Regular JOIN hides skills that NO student has yet.
-- LEFT JOIN keeps ALL skills even if total_students = 0.
-- WHY SUM(condition)?
-- In MySQL, TRUE = 1 and FALSE = 0.
-- SUM(proficiency_level = 'Beginner') counts matching rows.

-- ============================================================
-- QUERY 7: Students with MOST SKILLS (ranking)
-- ============================================================
SELECT
    s.student_id,
    s.name,
    d.dept_name,
    COUNT(ss.skill_id) AS total_skills
FROM Student s
JOIN Department d     ON s.dept_id    = d.dept_id
LEFT JOIN Student_Skill ss ON s.student_id = ss.student_id
GROUP BY s.student_id, s.name, d.dept_name
ORDER BY total_skills DESC
LIMIT 5;



-- ============================================================
-- QUERY 9: Skill tools for a specific skill (multi-valued)
-- ============================================================
SELECT
    sk.skill_name,
    st.tool_name
FROM Skill sk
JOIN Skill_Tools st ON sk.skill_id = st.skill_id
WHERE sk.skill_name = 'Python';


-- ============================================================
-- QUERY 10: UndergradStudent full profile (specialization)
-- ============================================================
SELECT
    s.student_id,
    s.name,
    s.email,
    d.dept_name,
    u.cgpa,
    u.credit_completed,
    u.year_of_study
FROM Student s
JOIN Department d         ON s.dept_id    = d.dept_id
JOIN UndergradStudent u   ON s.student_id = u.student_id
ORDER BY u.cgpa DESC;


-- ============================================================
-- QUERY 11: GradStudent full profile (specialization)
-- ============================================================
SELECT
    s.student_id,
    s.name,
    s.email,
    d.dept_name,
    g.thesis_topic,
    g.supervisor,
    g.research_area
FROM Student s
JOIN Department d       ON s.dept_id    = d.dept_id
JOIN GradStudent g      ON s.student_id = g.student_id;



-- ============================================================
-- QUERY 12: All events with their organizing club
-- ============================================================
SELECT
    e.event_id,
    e.event_name,
    e.event_date,
    e.location,
    e.max_participants,
    c.club_name
FROM Event e
JOIN Club c ON e.club_id = c.club_id
ORDER BY e.event_date;



-- ============================================================
-- QUERY 13: Event participation COUNT report
-- ============================================================
SELECT
    e.event_name,
    c.club_name,
    e.event_date,
    COUNT(p.student_id)                        AS total_registered,
    SUM(p.status = 'Attended')                 AS attended,
    SUM(p.status = 'Cancelled')                AS cancelled,
    e.max_participants,
    ROUND(
        COUNT(p.student_id) * 100.0
        / e.max_participants, 1
    )                                          AS fill_percentage
FROM Event e
JOIN Club c         ON e.club_id  = c.club_id
LEFT JOIN Participation p ON e.event_id = p.event_id
GROUP BY e.event_id, e.event_name, c.club_name,
         e.event_date, e.max_participants
ORDER BY total_registered DESC;



-- ============================================================
-- QUERY 14: MOST ACTIVE STUDENT report
-- ============================================================
SELECT
    s.student_id,
    s.name,
    d.dept_name,
    COUNT(p.event_id)              AS events_attended,
    SUM(p.status = 'Attended')     AS confirmed_attended
FROM Student s
JOIN Department d        ON s.dept_id    = d.dept_id
LEFT JOIN Participation p ON s.student_id = p.student_id
GROUP BY s.student_id, s.name, d.dept_name
ORDER BY events_attended DESC
LIMIT 5;

