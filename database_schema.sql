-- TEST ARENA Database Schema
-- Create Database
CREATE DATABASE IF NOT EXISTS test_arena;
USE test_arena;

-- User Table
CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Category/Exam Table
CREATE TABLE Exam (
    exam_id INT AUTO_INCREMENT PRIMARY KEY,
    exam_name VARCHAR(50) NOT NULL UNIQUE,
    duration_minutes INT NOT NULL,
    total_questions INT NOT NULL,
    description TEXT
);

-- Subject Table
CREATE TABLE Subject (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50) NOT NULL,
    exam_id INT,
    question_count INT,
    FOREIGN KEY (exam_id) REFERENCES Exam(exam_id) ON DELETE CASCADE
);

-- Question Table
CREATE TABLE Question (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    exam_id INT NOT NULL,
    subject_id INT NOT NULL,
    question_text TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_option CHAR(1) NOT NULL CHECK (correct_option IN ('A', 'B', 'C', 'D')),
    solution TEXT,
    difficulty_level ENUM('Easy', 'Medium', 'Hard') DEFAULT 'Medium',
    FOREIGN KEY (exam_id) REFERENCES Exam(exam_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES Subject(subject_id) ON DELETE CASCADE
);

-- Score Table
CREATE TABLE Score (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    exam_id INT NOT NULL,
    mode ENUM('Exam', 'Free Trial') NOT NULL,
    attempt_number INT DEFAULT 1,
    total_marks INT NOT NULL,
    correct_answers INT NOT NULL,
    wrong_answers INT NOT NULL,
    unanswered INT DEFAULT 0,
    time_taken_minutes INT,
    attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES Exam(exam_id) ON DELETE CASCADE
);

-- User Answers Table (Optional - for detailed tracking)
CREATE TABLE UserAnswer (
    answer_id INT AUTO_INCREMENT PRIMARY KEY,
    score_id INT NOT NULL,
    question_id INT NOT NULL,
    selected_option CHAR(1) CHECK (selected_option IN ('A', 'B', 'C', 'D', 'N')),
    is_correct BOOLEAN,
    FOREIGN KEY (score_id) REFERENCES Score(score_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES Question(question_id) ON DELETE CASCADE
);

-- Insert Sample Exams
INSERT INTO Exam (exam_name, duration_minutes, total_questions, description) VALUES
('PSC', 90, 100, 'Public Service Commission Exam'),
('UPSC', 120, 100, 'Union Public Service Commission Exam'),
('KEAM', 150, 100, 'Kerala Engineering Architecture Medical Exam'),
('NEET', 180, 100, 'National Eligibility cum Entrance Test'),
('JEE', 180, 100, 'Joint Entrance Examination');

-- Insert Sample Subjects for each exam
-- PSC Subjects
INSERT INTO Subject (subject_name, exam_id, question_count) VALUES
('General Knowledge', 1, 40),
('Current Affairs', 1, 30),
('Mathematics', 1, 30);

-- UPSC Subjects
INSERT INTO Subject (subject_name, exam_id, question_count) VALUES
('General Studies', 2, 50),
('Current Affairs', 2, 30),
('History', 2, 20);

-- KEAM Subjects
INSERT INTO Subject (subject_name, exam_id, question_count) VALUES
('Mathematics', 3, 40),
('Physics', 3, 30),
('Chemistry', 3, 30);

-- NEET Subjects
INSERT INTO Subject (subject_name, exam_id, question_count) VALUES
('Physics', 4, 25),
('Chemistry', 4, 25),
('Biology', 4, 50);

-- JEE Subjects
INSERT INTO Subject (subject_name, exam_id, question_count) VALUES
('Mathematics', 5, 34),
('Physics', 5, 33),
('Chemistry', 5, 33);

-- Sample Questions (Add more as needed)
-- PSC Sample Questions
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(1, 1, 'Who is the first President of India?', 'Dr. Rajendra Prasad', 'Dr. S. Radhakrishnan', 'Dr. Zakir Hussain', 'V.V. Giri', 'A', 'Dr. Rajendra Prasad was the first President of India from 1950 to 1962.'),
(1, 1, 'Capital of Kerala?', 'Kochi', 'Thiruvananthapuram', 'Kozhikode', 'Thrissur', 'B', 'Thiruvananthapuram is the capital city of Kerala.'),
(1, 3, 'What is 15 + 25?', '30', '35', '40', '45', 'C', '15 + 25 = 40');

-- NEET Sample Questions
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(4, 10, 'What is the powerhouse of the cell?', 'Nucleus', 'Mitochondria', 'Ribosome', 'Golgi Body', 'B', 'Mitochondria is known as the powerhouse of the cell as it generates ATP.'),
(4, 9, 'Which acid is found in vinegar?', 'Citric acid', 'Acetic acid', 'Tartaric acid', 'Oxalic acid', 'B', 'Vinegar contains acetic acid (CH3COOH).');

-- Create indexes for better performance
CREATE INDEX idx_username ON User(username);
CREATE INDEX idx_exam_id ON Question(exam_id);
CREATE INDEX idx_user_score ON Score(user_id, exam_id);
CREATE INDEX idx_score_date ON Score(attempt_date);
