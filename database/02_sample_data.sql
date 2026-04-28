-- inserting values in Department table
INSERT INTO Department (dept_name, dept_code) VALUES
('Computer Science & Engineering',  'CSE'),
('Business Administration',         'BBA'),
('Economics & Social Sciences',     'ECO'),
('English & Humanities',            'ENG'),
('Mathematics & Natural Sciences',  'MAT'),
('Electrical & Electronics Eng.',   'EEE'),
('Architecture',                    'ARC');

-- inserting values in Skill table
-- 15 skills across 7 categories
INSERT INTO Skill (skill_name, category) VALUES
('Python',              'Programming'),
('Java',                'Programming'),
('SQL',                 'Database'),
('Figma',               'Design'),
('Web Development',     'Programming'),
('Data Analysis',       'Analytics'),
('Public Speaking',     'Soft Skill'),
('Machine Learning',    'AI/ML'),
('Graphic Design',      'Design'),
('Leadership',          'Soft Skill'),
('C++',                 'Programming'),
('Excel',               'Analytics'),
('Video Editing',       'Media'),
('Project Management',  'Soft Skill'),
('Cybersecurity',       'Security');


-- inserting values in Skill_Tools table
INSERT INTO Skill_Tools (skill_id, tool_name) 
VALUES
-- Python (skill_id = 1)
(1, 'Django'),
(1, 'Flask'),
(1, 'NumPy'),
(1, 'Pandas'),
-- Java (skill_id = 2)
(2, 'Spring Boot'),
(2, 'Maven'),
-- SQL (skill_id = 3)
(3, 'MySQL Workbench'),
(3, 'PostgreSQL'),
-- Figma (skill_id = 4)
(4, 'FigJam'),
(4, 'Protopie'),
-- Web Development (skill_id = 5)
(5, 'React'),
(5, 'HTML/CSS'),
(5, 'Node.js'),
-- Data Analysis (skill_id = 6)
(6, 'Tableau'),
(6, 'Power BI'),
(6, 'Google Sheets'),
-- Machine Learning (skill_id = 8)
(8, 'TensorFlow'),
(8, 'Scikit-learn'),
(8, 'Keras'),
-- Graphic Design (skill_id = 9)
(9, 'Adobe Photoshop'),
(9, 'Canva'),
(9, 'Illustrator'),
-- Cybersecurity (skill_id = 15)
(15, 'Kali Linux'),
(15, 'Wireshark'),
(15, 'Metasploit');


-- inserting values in Club table
INSERT INTO Club (club_name, description, founding_year) VALUES
('BRAC Programming Club',
    'Competitive programming, hackathons, and coding workshops',     2015),
('BRAC Debate Club',
    'Parliamentary debate tournaments and public speaking training', 2012),
('BRAC Business Club',
    'Entrepreneurship competitions and business case events',        2014),
('BRAC Cultural Club',
    'Art, music, drama and cultural celebrations',                   2010),
('BRAC Robotics Club',
    'Robotics competitions, IoT projects and maker events',          2018),
('BRAC Photography Club',
    'Photography walks, editing workshops and exhibitions',          2019);
    
    



-- inserting values in Student table
-- 10 students across different departments
-- student_id 1–7  → UndergradStudent
-- student_id 8–10 → GradStudent
-- (We will specify this in next INSERT)
INSERT INTO Student (name, email, phone, enrollment_year, dept_id)
VALUES
-- Undergrads (will go into UndergradStudent table)
('Arif Hossain',     'arif@bracu.ac.bd',      '01711000001', 2022, 1),
('Nusrat Jahan',     'nusrat@bracu.ac.bd',    '01711000002', 2021, 1),
('Tanvir Ahmed',     'tanvir@bracu.ac.bd',    '01711000003', 2022, 2),
('Sumaiya Khan',     'sumaiya@bracu.ac.bd',   '01711000004', 2023, 3),
('Rafiq Islam',      'rafiq@bracu.ac.bd',     '01711000005', 2020, 1),
('Priya Sharma',     'priya@bracu.ac.bd',     '01711000006', 4,    4),
('Mehedi Hassan',    'mehedi@bracu.ac.bd',    '01711000007', 2021, 2),
-- Grad students (will go into GradStudent table)
('Dr. Lamia Akter',  'lamia@bracu.ac.bd',     '01711000008', 2019, 1),
('Karim Uddin',      'karim@bracu.ac.bd',     '01711000009', 2020, 6),
('Shirin Akhter',    'shirin@bracu.ac.bd',    '01711000010', 2018, 1);



-- inserting values in Event table
INSERT INTO Event (event_name, event_date, location, max_participants, club_id)
VALUES
('National Hackathon 2024',       '2024-03-15', 'UB40 Auditorium',   200, 1),
('Python Bootcamp',               '2024-04-10', 'Lab Room 301',       50,  1),
('Inter-Uni Debate Championship', '2024-03-20', 'Main Auditorium',    150, 2),
('Business Plan Competition',     '2024-04-25', 'Conference Hall A',  100, 3),
('Annual Cultural Night',         '2024-05-01', 'Open Playground',    500, 4),
('AI & ML Seminar',               '2024-05-15', 'UB40 Auditorium',    100, 1),
('Robotics Showcase 2024',        '2024-06-10', 'Engineering Lab',     80, 5),
('Photo Walk — Old Dhaka',        '2024-06-20', 'Sadarghat, Dhaka',    40, 6),
('Startup Pitch Night',           '2024-07-05', 'Conference Hall B',   75, 3),
('Code for Change Hackathon',     '2024-08-01', 'UB40 Auditorium',    180, 1);



-- inserting values in UndergradStudent table
-- student_id MUST already exist in Student table
-- student_id 1–7 are undergrads
INSERT INTO UndergradStudent (student_id, cgpa, credit_completed, year_of_study)
VALUES
(1,  3.85,  90,  3),   -- Arif      — 3rd year, strong CGPA
(2,  3.60,  75,  3),   -- Nusrat    — 3rd year
(3,  3.20,  60,  2),   -- Tanvir    — 2nd year
(4,  3.45,  30,  1),   -- Sumaiya   — 1st year
(5,  3.90, 120,  4),   -- Rafiq     — 4th year (senior)
(6,  3.10,  45,  2),   -- Priya     — 2nd year
(7,  3.55,  70,  3);   -- Mehedi    — 3rd year




-- inserting values in GradStudent table
-- student_id 8–10 are grad students
INSERT INTO GradStudent (student_id, thesis_topic, supervisor, research_area)
VALUES
(8,
 'Deep Learning for Bangla NLP',
 'Prof. Md. Kamal Hossain',
 'Natural Language Processing'),

(9,
 'IoT-based Smart Grid Optimization',
 'Prof. Nasrin Sultana',
 'Internet of Things'),

(10,
 'Federated Learning in Healthcare',
 'Prof. Zahir Ahmed',
 'Privacy-Preserving Machine Learning');




-- inserting values in Student_skill table
INSERT INTO Student_Skill (student_id, skill_id, proficiency_level, acquired_date)
VALUES
-- Arif (student 1) — CSE, strong coder
(1, 1,  'Advanced',      '2023-01-15'),  -- Python
(1, 3,  'Intermediate',  '2023-03-10'),  -- SQL
(1, 8,  'Beginner',      '2024-01-01'),  -- ML
(1, 5,  'Intermediate',  '2023-06-01'),  -- Web Dev

-- Nusrat (student 2) — Design + Programming
(2, 1,  'Intermediate',  '2022-06-20'),  -- Python
(2, 4,  'Advanced',      '2021-09-01'),  -- Figma
(2, 9,  'Advanced',      '2022-01-15'),  -- Graphic Design
(2, 5,  'Beginner',      '2023-08-10'),  -- Web Dev

-- Tanvir (student 3) — Business + Soft Skills
(3, 7,  'Advanced',      '2021-05-10'),  -- Public Speaking
(3, 10, 'Intermediate',  '2022-02-20'),  -- Leadership
(3, 14, 'Intermediate',  '2023-01-01'),  -- Project Mgmt

-- Sumaiya (student 4) — Analytics
(4, 6,  'Beginner',      '2023-08-01'),  -- Data Analysis
(4, 12, 'Intermediate',  '2023-05-15'),  -- Excel

-- Rafiq (student 5) — Senior CSE, multi-skilled
(5, 1,  'Advanced',      '2020-01-01'),  -- Python
(5, 2,  'Advanced',      '2020-06-15'),  -- Java
(5, 8,  'Intermediate',  '2023-01-01'),  -- ML
(5, 11, 'Advanced',      '2021-03-01'),  -- C++
(5, 15, 'Beginner',      '2024-01-01'),  -- Cybersecurity

-- Priya (student 6) — Creative
(6, 7,  'Advanced',      '2022-11-01'),  -- Public Speaking
(6, 9,  'Intermediate',  '2023-03-01'),  -- Graphic Design
(6, 13, 'Advanced',      '2022-06-01'),  -- Video Editing

-- Mehedi (student 7) — Business focused
(7, 5,  'Intermediate',  '2022-04-10'),  -- Web Dev
(7, 14, 'Beginner',      '2023-01-01'),  -- Project Mgmt

-- Grad students
(8,  1,  'Advanced',     '2019-01-01'),  -- Lamia — Python
(8,  8,  'Advanced',     '2020-01-01'),  -- Lamia — ML
(9,  11, 'Advanced',     '2020-06-01'),  -- Karim — C++
(9,  15, 'Intermediate', '2021-01-01'),  -- Karim — Cybersec
(10, 8,  'Advanced',     '2018-06-01'),  -- Shirin — ML
(10, 1,  'Advanced',     '2019-01-01');  -- Shirin — Python



-- inserting values in Participation table
INSERT INTO Participation
    (student_id, event_id, registration_date, status)
VALUES
-- National Hackathon (event 1)
(1, 1,  '2024-03-01', 'Attended'),
(2, 1,  '2024-03-02', 'Attended'),
(5, 1,  '2024-03-01', 'Attended'),
(8, 1,  '2024-03-01', 'Attended'),
(10,1,  '2024-03-02', 'Attended'),

-- Python Bootcamp (event 2)
(1, 2,  '2024-04-01', 'Attended'),
(4, 2,  '2024-04-02', 'Registered'),
(8, 2,  '2024-04-01', 'Attended'),

-- Debate Championship (event 3)
(3, 3,  '2024-03-05', 'Attended'),
(6, 3,  '2024-03-06', 'Attended'),

-- Business Plan Competition (event 4)
(3, 4,  '2024-04-15', 'Attended'),
(4, 4,  '2024-04-16', 'Registered'),
(7, 4,  '2024-04-16', 'Attended'),

-- Cultural Night (event 5)
(2, 5,  '2024-04-20', 'Attended'),
(3, 5,  '2024-04-22', 'Attended'),
(6, 5,  '2024-04-23', 'Attended'),

-- AI & ML Seminar (event 6)
(1, 6,  '2024-05-10', 'Attended'),
(5, 6,  '2024-05-10', 'Attended'),
(8, 6,  '2024-05-11', 'Attended'),
(10,6,  '2024-05-11', 'Attended'),

-- Robotics Showcase (event 7)
(5, 7,  '2024-06-01', 'Attended'),
(9, 7,  '2024-06-02', 'Attended'),

-- Photo Walk (event 8)
(6, 8,  '2024-06-15', 'Attended'),
(2, 8,  '2024-06-15', 'Registered'),

-- Startup Pitch Night (event 9)
(3, 9,  '2024-06-25', 'Attended'),
(7, 9,  '2024-06-26', 'Attended'),

-- Code for Change Hackathon (event 10)
(1, 10, '2024-07-20', 'Registered'),
(5, 10, '2024-07-20', 'Registered'),
(8, 10, '2024-07-21', 'Registered'),
(9, 10, '2024-07-21', 'Registered');



INSERT INTO club_membership (student_id, club_id, joined_date, role)
VALUES
-- Programming Club (club 1)
(1, 1, '2022-09-01', 'President'),
(2, 1, '2022-09-05', 'Member'),
(5, 1, '2020-09-01', 'Coordinator'),
(8, 1, '2019-09-01', 'Member'),

-- Debate Club (club 2)
(3, 2, '2022-09-01', 'President'),
(6, 2, '2022-09-10', 'Secretary'),
(4, 2, '2023-09-01', 'Member'),

-- Business Club (club 3)
(7, 3, '2021-09-01', 'Vice President'),
(3, 3, '2022-09-15', 'Member'),
(4, 3, '2023-09-05', 'Member'),

-- Cultural Club (club 4)
(6, 4, '2022-09-01', 'Coordinator'),
(2, 4, '2022-10-01', 'Member'),

-- Robotics Club (club 5)
(5, 5, '2020-09-01', 'President'),
(9, 5, '2020-10-01', 'Coordinator'),

-- Photography Club (club 6)
(6, 6, '2019-09-01', 'President'),
(2, 6, '2022-09-01', 'Member');
