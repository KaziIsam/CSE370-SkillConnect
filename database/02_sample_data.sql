USE skillconnect;

-- ============================================================
-- INSERT 1: Department (7 departments)
-- ============================================================
INSERT INTO Department (dept_name, dept_code) VALUES
('Computer Science & Engineering',  'CSE'),
('Business Administration',         'BBA'),
('Economics & Social Sciences',     'ECO'),
('English & Humanities',            'ENG'),
('Mathematics & Natural Sciences',  'MAT'),
('Electrical & Electronics Eng.',   'EEE'),
('Architecture',                    'ARC');

-- ============================================================
-- INSERT 2: Skill (15 skills)
-- ============================================================
INSERT INTO Skill (skill_name, category) VALUES
('Python',           'Programming'),
('Java',             'Programming'),
('SQL',              'Database'),
('Figma',            'Design'),
('Web Development',  'Programming'),
('Data Analysis',    'Analytics'),
('Public Speaking',  'Soft Skill'),
('Machine Learning', 'AI/ML'),
('Graphic Design',   'Design'),
('Leadership',       'Soft Skill'),
('C++',              'Programming'),
('Excel',            'Analytics'),
('Video Editing',    'Media'),
('Project Management','Soft Skill'),
('Cybersecurity',    'Security');

-- ============================================================
-- INSERT 3: Skill_Tools (multi-valued attribute)
-- ============================================================
INSERT INTO Skill_Tools (skill_id, tool_name) VALUES
(1, 'Django'),   (1, 'Flask'),    (1, 'NumPy'),   (1, 'Pandas'),
(2, 'Spring Boot'), (2, 'Maven'),
(3, 'MySQL Workbench'), (3, 'PostgreSQL'),
(4, 'FigJam'),   (4, 'Protopie'),
(5, 'React'),    (5, 'HTML/CSS'), (5, 'Node.js'),
(6, 'Tableau'),  (6, 'Power BI'), (6, 'Google Sheets'),
(8, 'TensorFlow'), (8, 'Scikit-learn'), (8, 'Keras'),
(9, 'Photoshop'), (9, 'Canva'),  (9, 'Illustrator'),
(15,'Kali Linux'),(15,'Wireshark'),(15,'Metasploit');

-- ============================================================
-- INSERT 4: Club (6 clubs)
-- ============================================================
INSERT INTO Club (club_name, description, founding_year) VALUES
('BRAC Programming Club',  'Coding competitions and workshops',        2015),
('BRAC Debate Club',       'Debate tournaments and public speaking',   2012),
('BRAC Business Club',     'Entrepreneurship and business events',     2014),
('BRAC Cultural Club',     'Art, music and cultural celebrations',     2010),
('BRAC Robotics Club',     'Robotics competitions and IoT projects',   2018),
('BRAC Photography Club',  'Photography walks and exhibitions',        2019);

-- ============================================================
-- INSERT 5: Student (10 students)
-- dept_id: CSE=1, BBA=2, ECO=3, ENG=4, MAT=5, EEE=6, ARC=7
-- students 1-7 = Undergrad, students 8-10 = Grad
-- ============================================================
INSERT INTO Student (name, email, phone, enrollment_year, dept_id) VALUES
('Arif Hossain',    'arif@bracu.ac.bd',    '01711000001', 2022, 1),
('Nusrat Jahan',    'nusrat@bracu.ac.bd',  '01711000002', 2021, 1),
('Tanvir Ahmed',    'tanvir@bracu.ac.bd',  '01711000003', 2022, 2),
('Sumaiya Khan',    'sumaiya@bracu.ac.bd', '01711000004', 2023, 3),
('Rafiq Islam',     'rafiq@bracu.ac.bd',   '01711000005', 2020, 1),
('Priya Sharma',    'priya@bracu.ac.bd',   '01711000006', 2022, 4),
('Mehedi Hassan',   'mehedi@bracu.ac.bd',  '01711000007', 2021, 2),
('Lamia Akter',     'lamia@bracu.ac.bd',   '01711000008', 2019, 1),
('Karim Uddin',     'karim@bracu.ac.bd',   '01711000009', 2020, 6),
('Shirin Akhter',   'shirin@bracu.ac.bd',  '01711000010', 2018, 1);

-- ============================================================
-- INSERT 6: Event (10 events)
-- ============================================================
INSERT INTO Event (event_name, event_date, location, max_participants, club_id) VALUES
('National Hackathon 2024',       '2024-03-15', 'UB40 Auditorium',   200, 1),
('Python Bootcamp',               '2024-04-10', 'Lab Room 301',       50,  1),
('Inter-Uni Debate Championship', '2024-03-20', 'Main Auditorium',   150,  2),
('Business Plan Competition',     '2024-04-25', 'Conference Hall A', 100,  3),
('Annual Cultural Night',         '2024-05-01', 'Open Playground',   500,  4),
('AI & ML Seminar',               '2024-05-15', 'UB40 Auditorium',   100,  1),
('Robotics Showcase 2024',        '2024-06-10', 'Engineering Lab',    80,  5),
('Photo Walk Old Dhaka',          '2024-06-20', 'Sadarghat Dhaka',    40,  6),
('Startup Pitch Night',           '2024-07-05', 'Conference Hall B',  75,  3),
('Code for Change Hackathon',     '2024-08-01', 'UB40 Auditorium',   180,  1);

-- ============================================================
-- INSERT 7: UndergradStudent (students 1-7)
-- ============================================================
INSERT INTO UndergradStudent (student_id, cgpa, credit_completed, year_of_study) VALUES
(1,  3.85,  90,  3),
(2,  3.60,  75,  3),
(3,  3.20,  60,  2),
(4,  3.45,  30,  1),
(5,  3.90, 120,  4),
(6,  3.10,  45,  2),
(7,  3.55,  70,  3);

-- ============================================================
-- INSERT 8: GradStudent (students 8-10)
-- ============================================================
INSERT INTO GradStudent (student_id, thesis_topic, supervisor, research_area) VALUES
(8,  'Deep Learning for Bangla NLP',
     'Prof. Md. Kamal Hossain',  'Natural Language Processing'),
(9,  'IoT-based Smart Grid Optimization',
     'Prof. Nasrin Sultana',     'Internet of Things'),
(10, 'Federated Learning in Healthcare',
     'Prof. Zahir Ahmed',        'Privacy-Preserving ML');

-- ============================================================
-- INSERT 9: Student_Skill (29 skill assignments)
-- ============================================================
INSERT INTO Student_Skill (student_id, skill_id, proficiency_level, acquired_date) VALUES
-- Arif (1)
(1, 1,  'Advanced',      '2023-01-15'),
(1, 3,  'Intermediate',  '2023-03-10'),
(1, 8,  'Beginner',      '2024-01-01'),
(1, 5,  'Intermediate',  '2023-06-01'),
-- Nusrat (2)
(2, 1,  'Intermediate',  '2022-06-20'),
(2, 4,  'Advanced',      '2021-09-01'),
(2, 9,  'Advanced',      '2022-01-15'),
(2, 5,  'Beginner',      '2023-08-10'),
-- Tanvir (3)
(3, 7,  'Advanced',      '2021-05-10'),
(3, 10, 'Intermediate',  '2022-02-20'),
(3, 14, 'Intermediate',  '2023-01-01'),
-- Sumaiya (4)
(4, 6,  'Beginner',      '2023-08-01'),
(4, 12, 'Intermediate',  '2023-05-15'),
-- Rafiq (5)
(5, 1,  'Advanced',      '2020-01-01'),
(5, 2,  'Advanced',      '2020-06-15'),
(5, 8,  'Intermediate',  '2023-01-01'),
(5, 11, 'Advanced',      '2021-03-01'),
(5, 15, 'Beginner',      '2024-01-01'),
-- Priya (6)
(6, 7,  'Advanced',      '2022-11-01'),
(6, 9,  'Intermediate',  '2023-03-01'),
(6, 13, 'Advanced',      '2022-06-01'),
-- Mehedi (7)
(7, 5,  'Intermediate',  '2022-04-10'),
(7, 14, 'Beginner',      '2023-01-01'),
-- Grad students
(8, 1,  'Advanced',      '2019-01-01'),
(8, 8,  'Advanced',      '2020-01-01'),
(9, 11, 'Advanced',      '2020-06-01'),
(9, 15, 'Intermediate',  '2021-01-01'),
(10, 8, 'Advanced',      '2018-06-01'),
(10, 1, 'Advanced',      '2019-01-01');

-- ============================================================
-- INSERT 10: Participation (30 registrations)
-- ============================================================
INSERT INTO Participation (student_id, event_id, registration_date, status) VALUES
(1,1,'2024-03-01','Attended'),  (2,1,'2024-03-02','Attended'),
(5,1,'2024-03-01','Attended'),  (8,1,'2024-03-01','Attended'),
(10,1,'2024-03-02','Attended'),
(1,2,'2024-04-01','Attended'),  (4,2,'2024-04-02','Registered'),
(8,2,'2024-04-01','Attended'),
(3,3,'2024-03-05','Attended'),  (6,3,'2024-03-06','Attended'),
(3,4,'2024-04-15','Attended'),  (4,4,'2024-04-16','Registered'),
(7,4,'2024-04-16','Attended'),
(2,5,'2024-04-20','Attended'),  (3,5,'2024-04-22','Attended'),
(6,5,'2024-04-23','Attended'),
(1,6,'2024-05-10','Attended'),  (5,6,'2024-05-10','Attended'),
(8,6,'2024-05-11','Attended'),  (10,6,'2024-05-11','Attended'),
(5,7,'2024-06-01','Attended'),  (9,7,'2024-06-02','Attended'),
(6,8,'2024-06-15','Attended'),  (2,8,'2024-06-15','Registered'),
(3,9,'2024-06-25','Attended'),  (7,9,'2024-06-26','Attended'),
(1,10,'2024-07-20','Registered'),(5,10,'2024-07-20','Registered'),
(8,10,'2024-07-21','Registered'),(9,10,'2024-07-21','Registered');

-- ============================================================
-- INSERT 11: ClubMembership (16 memberships)
-- ============================================================
INSERT INTO ClubMembership (student_id, club_id, joined_date, role) VALUES
(1,1,'2022-09-01','President'),
(2,1,'2022-09-05','Member'),
(5,1,'2020-09-01','Coordinator'),
(8,1,'2019-09-01','Member'),
(3,2,'2022-09-01','President'),
(6,2,'2022-09-10','Secretary'),
(4,2,'2023-09-01','Member'),
(7,3,'2021-09-01','Vice President'),
(3,3,'2022-09-15','Member'),
(4,3,'2023-09-05','Member'),
(6,4,'2022-09-01','Coordinator'),
(2,4,'2022-10-01','Member'),
(5,5,'2020-09-01','President'),
(9,5,'2020-10-01','Coordinator'),
(6,6,'2019-09-01','President'),
(2,6,'2022-09-01','Member');

-- ============================================================
-- VERIFY: Check row counts
-- ============================================================
SELECT 'Department'    AS tbl, COUNT(*) AS total FROM Department    UNION ALL
SELECT 'Skill',                COUNT(*)           FROM Skill         UNION ALL
SELECT 'Club',                 COUNT(*)           FROM Club          UNION ALL
SELECT 'Student',              COUNT(*)           FROM Student       UNION ALL
SELECT 'Event',                COUNT(*)           FROM Event         UNION ALL
SELECT 'UndergradStudent',     COUNT(*)           FROM UndergradStudent UNION ALL
SELECT 'GradStudent',          COUNT(*)           FROM GradStudent   UNION ALL
SELECT 'Student_Skill',        COUNT(*)           FROM Student_Skill UNION ALL
SELECT 'Participation',        COUNT(*)           FROM Participation UNION ALL
SELECT 'ClubMembership',       COUNT(*)           FROM ClubMembership;