create database Skill_Connect;
use Skill_Connect;

-- TABLE-01: Department
CREATE TABLE Department(
	dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    dept_code VARCHAR(10) NOT NULL UNIQUE
);

-- TABLE-02: Skill
CREATE TABLE Skill(
	skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL
);

-- TABLE-02B: skill_tools
-- Implements the MULTI-VALUED attribute "skill_tools" inside SKill entity
CREATE TABLE skill_tools(
	skill_id INT NOT NULL,
    tool_name VARCHAR(100) NOT NULL,
    
    PRIMARY KEY(skill_id , tool_name),			-- composite pk as the same tool cannot appear twice under the same skill
    
    FOREIGN KEY(skill_id) REFERENCES Skill(skill_id) ON DELETE CASCADE
);

-- TABLE-03: Club
CREATE TABLE Club(
	club_id     	INT 			AUTO_INCREMENT PRIMARY KEY,
    club_name   	VARCHAR(100)    NOT NULL UNIQUE,
    description 	TEXT,
    founding_year   YEAR
);

-- TABLE-04: Student
-- depends on Department
CREATE TABLE Student(
	student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15),
    enrollment_year YEAR NOT NULL,
    dept_id INT NOT NULL,
    
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

-- TABLE-05: Event
-- depends on CLub
CREATE TABLE EVENT(
	event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,
    location VARCHAR(100),
    max_participants INT NOT NULL DEFAULT 100,
    club_id INT NOT NULL,
    
    CONSTRAINT chk_max_participants CHECK (max_participants > 0),
    
    FOREIGN KEY (club_id) REFERENCES Club(club_id)
    ON DELETE RESTRICT
);


-- ============================================================
-- SPECIALIZATON SUB-TYPES
-- ============================================================
-- TABLE-06: UndergradStudent
CREATE TABLE UndergradStudent(
	student_id INT PRIMARY KEY,
    cgpa DECIMAL(3,2) NOT NULL DEFAULT 0.00,
    credit_completed INT NOT NULL DEFAULT 0,
    year_of_study INT NOT NULL,
    
    CONSTRAINT chk_cgpa CHECK(cgpa >= 0.00 AND cgpa <= 4.00),
    CONSTRAINT chk_year_of_study CHECK(year_of_study BETWEEN 1 AND 6),
    
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
    ON DELETE CASCADE
);

-- TABLE-07: GradStudent
CREATE TABLE GradStudent(
	student_id INT PRIMARY KEY,
    thesis_topic VARCHAR(200),
    supervisor	VARCHAR(100) NOT NULL,
    research_area VARCHAR(100),
    
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
    ON DELETE CASCADE
);


-- ============================================================
-- Junction and Weak tables 
-- ============================================================
-- TABLE_08: student_skill (junction - M:N)
-- depends on Student and Skill
CREATE TABLE student_skill(
	student_id INT NOT NULL,
    skill_id INT NOT NULL,
    proficiency_level ENUM(
		'Beginner',
        'Intermediate',
        'Advanced'
	)  		NOT NULL,
    acquired_date DATE,
    
    PRIMARY KEY(student_id , skill_id),
    
    FOREIGN KEY(student_id) REFERENCES Student(student_id)
    ON DELETE CASCADE,
    FOREIGN KEY(skill_id) REFERENCES Skill(skill_id)
    ON DELETE CASCADE
);

-- TABLE-09: Participation (junction - M:N)
-- depends onStudent and Event
CREATE TABLE Participation(
	student_id INT NOT NULL,
    event_id INT NOT NULL,
    registration_date DATE DEFAULT(CURRENT_DATE),
    status ENUM(
		'Registered',
        'Attended',
        'Cancelled'
	)      	NOT NULL DEFAULT 'Registered',
    
    PRIMARY KEY(student_id , event_id),
    
    FOREIGN KEY(student_id) REFERENCES Student(student_id)
    ON DELETE CASCADE,
    FOREIGN KEY(event_id) REFERENCES Event(event_id)
    ON DELETE CASCADE
);

-- TABLE-10: club_membership ( associative entity )
CREATE TABLE club_membership(
	student_id INT NOT NULL,
    club_id INT NOT NULL,
    joined_date DATE NOT NULL DEFAULT(CURRENT_DATE),
    role ENUM(
		'Member',
		'Coordinator',
		'President',
		'Vice President',
		'Secretary'
	)      NOT NULL DEFAULT 'MEMBER',
    
    PRIMARY KEY(student_id,club_id),
    
    FOREIGN KEY(student_id) REFERENCES Student(student_id)
    ON DELETE CASCADE,
    FOREIGN KEY(club_id) REFERENCES Club(club_id)
    ON DELETE CASCADE
);

-- VIEW: Student_Total_Skills
-- Implementing the derived attribute "total_skill" of Student table
CREATE VIEW Student_Total_Skills AS
SELECT s.student_id , s.name , s.email , COUNT(ss.skill_id) AS total_skill
FROM student s
LEFT JOIN student_skill ss ON s.student_id = ss.student_id
GROUP BY s.student_id , s.name , s.email;