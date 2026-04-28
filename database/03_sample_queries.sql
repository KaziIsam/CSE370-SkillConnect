-- SAMPLE QUERIES for Student Skill Management System
SELECT 'Department'      AS tbl, COUNT(*) AS total FROM Department       UNION ALL
SELECT 'Skill',                  COUNT(*)           FROM Skill            UNION ALL
SELECT 'Club',                   COUNT(*)           FROM Club             UNION ALL
SELECT 'Student',                COUNT(*)           FROM Student          UNION ALL
SELECT 'Event',                  COUNT(*)           FROM Event            UNION ALL
SELECT 'UndergradStudent',       COUNT(*)           FROM UndergradStudent UNION ALL
SELECT 'GradStudent',            COUNT(*)           FROM GradStudent      UNION ALL
SELECT 'Student_Skill',          COUNT(*)           FROM Student_Skill    UNION ALL
SELECT 'Participation',          COUNT(*)           FROM Participation    UNION ALL
SELECT 'ClubMembership',         COUNT(*)           FROM club_membership;


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
-- This is analytics report 
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
-- QUERY 8: Derived attribute — total_skill using VIEW
-- Run this once to create the view
-- ============================================================
CREATE OR REPLACE VIEW Student_Total_Skills AS
SELECT
    s.student_id,
    s.name,
    s.email,
    d.dept_name,
    COUNT(ss.skill_id) AS total_skill
FROM Student s
JOIN Department d          ON s.dept_id    = d.dept_id
LEFT JOIN Student_Skill ss ON s.student_id = ss.student_id
GROUP BY s.student_id, s.name, s.email, d.dept_name;

-- Use the view like a table:
SELECT * FROM Student_Total_Skills
ORDER BY total_skill DESC;




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



--  MODULE 2 — Club & Event Queries
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




-- MODULE 3 — Participation & Analytics Queries
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



-- ============================================================
-- QUERY 15: MOST POPULAR CLUB report
-- ============================================================
SELECT
    c.club_name,
    COUNT(DISTINCT e.event_id)     AS total_events,
    COUNT(p.student_id)            AS total_participants,
    COUNT(DISTINCT cm.student_id)  AS total_members
FROM Club c
LEFT JOIN Event e           ON c.club_id  = e.club_id
LEFT JOIN Participation p   ON e.event_id = p.event_id
LEFT JOIN club_membership cm ON c.club_id = cm.club_id
GROUP BY c.club_id, c.club_name
ORDER BY total_participants DESC;



-- ============================================================
-- QUERY 16: Students who joined a specific club + their role
-- ============================================================
SELECT
    s.name,
    s.email,
    d.dept_name,
    cm.role,
    cm.joined_date
FROM Student s
JOIN Department d       ON s.dept_id    = d.dept_id
JOIN club_membership cm ON s.student_id = cm.student_id
JOIN Club c             ON cm.club_id   = c.club_id
WHERE c.club_name = 'BRAC Programming Club'
ORDER BY cm.joined_date;



-- ============================================================
-- QUERY 17: Students who have skills but joined NO events
-- Uses LEFT JOIN + NULL check
-- ============================================================
SELECT
    s.name,
    s.email,
    d.dept_name,
    COUNT(ss.skill_id) AS skills_count
FROM Student s
JOIN Department d          ON s.dept_id    = d.dept_id
JOIN Student_Skill ss      ON s.student_id = ss.student_id
LEFT JOIN Participation p  ON s.student_id = p.student_id
WHERE p.student_id IS NULL
GROUP BY s.student_id, s.name, s.email, d.dept_name;

-- WHY IS NULL?
-- LEFT JOIN keeps students even with no participation rows.
-- IS NULL filters to ONLY those with no participation.


-- ============================================================
-- QUERY 18: Skill gap — skills no CSE student has yet
-- Uses NOT IN subquery
-- ============================================================
SELECT skill_name, category
FROM Skill
WHERE skill_id NOT IN (
    SELECT DISTINCT ss.skill_id
    FROM Student_Skill ss
    JOIN Student s ON ss.student_id = s.student_id
    JOIN Department d ON s.dept_id = d.dept_id
    WHERE d.dept_code = 'CSE'
);


-- ============================================================
-- QUERY 19: Department-wise skill summary
-- ============================================================
SELECT
    d.dept_name,
    COUNT(DISTINCT s.student_id)   AS total_students,
    COUNT(DISTINCT ss.skill_id)    AS unique_skills,
    COUNT(ss.skill_id)             AS total_skill_entries,
    ROUND(
        COUNT(ss.skill_id) * 1.0
        / COUNT(DISTINCT s.student_id), 1
    )                              AS avg_skills_per_student
FROM Department d
LEFT JOIN Student s        ON d.dept_id    = s.dept_id
LEFT JOIN Student_Skill ss ON s.student_id = ss.student_id
GROUP BY d.dept_id, d.dept_name
ORDER BY avg_skills_per_student DESC;



-- ============================================================
-- QUERY 20: SEARCH across name, skill, department
-- (simulates a real search bar)
-- ============================================================
SELECT DISTINCT
    s.student_id,
    s.name,
    s.email,
    d.dept_name,
    sk.skill_name,
    ss.proficiency_level
FROM Student s
JOIN Department d      ON s.dept_id    = d.dept_id
JOIN Student_Skill ss  ON s.student_id = ss.student_id
JOIN Skill sk          ON ss.skill_id  = sk.skill_id
WHERE s.name      LIKE '%Arif%'    -- search by name
   OR sk.skill_name LIKE '%Python%' -- OR by skill
   OR d.dept_name   LIKE '%CSE%';   -- OR by department

-- WHY LIKE with %?
-- % means "anything before or after".
-- 'Python' matches 'Python', 'Python 3', 'Advanced Python'.
-- WHY DISTINCT?
-- Without it, a student with 3 skills matching
-- the search appears 3 times.