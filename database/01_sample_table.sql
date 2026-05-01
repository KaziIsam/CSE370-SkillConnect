CREATE DATABASE skillconnect CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE skillconnect;

-- TABLE 1: Department 
CREATE TABLE Department (
    dept_id   INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    dept_code VARCHAR(10)  NOT NULL UNIQUE
);


-- TABLE 2: Skill
CREATE TABLE Skill (
    skill_id   INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    category   VARCHAR(50)  NOT NULL
);


-- TABLE 3: Skill_Tools (multi-valued attribute)
CREATE TABLE Skill_Tools (
    skill_id  INT          NOT NULL,
    tool_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (skill_id, tool_name),
    FOREIGN KEY (skill_id) REFERENCES Skill(skill_id) ON DELETE CASCADE
);


-- TABLE 4: Club
CREATE TABLE Club (
    club_id       INT AUTO_INCREMENT PRIMARY KEY,
    club_name     VARCHAR(100) NOT NULL UNIQUE,
    description   TEXT,
    founding_year YEAR
);


-- TABLE 5: Student (depends on Department)
CREATE TABLE Student (
    student_id      INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(100) NOT NULL UNIQUE,
    phone           VARCHAR(15),
    enrollment_year YEAR         NOT NULL,
    dept_id         INT          NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);


-- TABLE 6: Event (depends on Club)
CREATE TABLE Event (
    event_id         INT AUTO_INCREMENT PRIMARY KEY,
    event_name       VARCHAR(100) NOT NULL,
    event_date       DATE         NOT NULL,
    location         VARCHAR(100),
    max_participants INT          NOT NULL DEFAULT 100,
    club_id          INT          NOT NULL,
    CONSTRAINT chk_max CHECK (max_participants > 0),
    FOREIGN KEY (club_id) REFERENCES Club(club_id) ON DELETE RESTRICT
);


-- TABLE 7: UndergradStudent 
CREATE TABLE UndergradStudent (
    student_id       INT            PRIMARY KEY,
    cgpa             DECIMAL(3,2)   NOT NULL DEFAULT 0.00,
    credit_completed INT            NOT NULL DEFAULT 0,
    year_of_study    INT            NOT NULL,
    CONSTRAINT chk_cgpa CHECK (cgpa >= 0.00 AND cgpa <= 4.00),
    CONSTRAINT chk_year CHECK (year_of_study BETWEEN 1 AND 6),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE
);


-- TABLE 8: GradStudent 
CREATE TABLE GradStudent (
    student_id    INT          PRIMARY KEY,
    thesis_topic  VARCHAR(200),
    supervisor    VARCHAR(100) NOT NULL,
    research_area VARCHAR(100),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE
);


-- TABLE 9: Student_Skill (junction — M:N)
CREATE TABLE Student_Skill (
    student_id        INT  NOT NULL,
    skill_id          INT  NOT NULL,
    proficiency_level ENUM('Beginner','Intermediate','Advanced') NOT NULL,
    acquired_date     DATE,
    PRIMARY KEY (student_id, skill_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id)   REFERENCES Skill(skill_id)     ON DELETE CASCADE
);


-- TABLE 10: Participation (junction — M:N)
CREATE TABLE Participation (
    student_id        INT  NOT NULL,
    event_id          INT  NOT NULL,
    registration_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    status            ENUM('Registered','Attended','Cancelled') NOT NULL DEFAULT 'Registered',
    PRIMARY KEY (student_id, event_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id)   REFERENCES Event(event_id)     ON DELETE CASCADE
);


-- TABLE 11: ClubMembership (associative entity)
CREATE TABLE ClubMembership (
    student_id  INT NOT NULL,
    club_id     INT NOT NULL,
    joined_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    role        ENUM('Member','Coordinator','President','Vice President','Secretary')
                NOT NULL DEFAULT 'Member',
    PRIMARY KEY (student_id, club_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (club_id)    REFERENCES Club(club_id)       ON DELETE CASCADE
);


-- VERIFY: Show all created tables
SHOW TABLES;