import sqlite3
import os
from database import Database

def setup():
    print("Setting up TEST ARENA database (SQLite)...")
    
    db = Database()
    
    # SQLite creates the file automatically if it doesn't exist when connecting
    if os.path.exists(db.database):
        print(f"Database file '{db.database}' already exists.")
    
    conn = sqlite3.connect(db.database)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    try:
        # Create Tables
        # User Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            phone VARCHAR(20)
        )
        """)
        
        # Exam Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Exam (
            exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_name VARCHAR(50) NOT NULL,
            duration_minutes INT NOT NULL,
            total_questions INT NOT NULL
        )
        """)
        
        # Subject Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Subject (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name VARCHAR(50) NOT NULL,
            exam_id INT,
            FOREIGN KEY (exam_id) REFERENCES Exam(exam_id)
        )
        """)
        
        # Question Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Question (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INT,
            subject_id INT,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option CHAR(1) NOT NULL,
            solution TEXT,
            FOREIGN KEY (exam_id) REFERENCES Exam(exam_id),
            FOREIGN KEY (subject_id) REFERENCES Subject(subject_id)
        )
        """)
        
        # Score Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Score (
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT,
            exam_id INT,
            mode VARCHAR(20),
            attempt_number INT,
            total_marks INT,
            correct_answers INT,
            wrong_answers INT,
            unanswered INT,
            time_taken_minutes INT,
            attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            FOREIGN KEY (exam_id) REFERENCES Exam(exam_id)
        )
        """)
        
        # UserAnswer Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserAnswer (
            answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            score_id INT,
            question_id INT,
            selected_option CHAR(1),
            is_correct BOOLEAN,
            FOREIGN KEY (score_id) REFERENCES Score(score_id),
            FOREIGN KEY (question_id) REFERENCES Question(question_id)
        )
        """)
        
        print("Tables created successfully.")
            
        # Insert Initial Data (Exams and Subjects)
        cursor.execute("SELECT COUNT(*) FROM Exam")
        if cursor.fetchone()[0] == 0:
            print("Inserting initial Exam and Subject data...")
            # Exams: ID, Name, Duration, Total Qs
            exams = [
                (1, 'PSC', 60, 100), 
                (2, 'UPSC', 120, 100), 
                (3, 'KEAM', 150, 120), 
                (4, 'NEET', 180, 180), 
                (5, 'JEE', 180, 90)
            ]
            cursor.executemany("INSERT INTO Exam (exam_id, exam_name, duration_minutes, total_questions) VALUES (?, ?, ?, ?)", exams)
            
            # Subjects: ID, Name, ExamID
            subjects = [
                (1, 'General Knowledge', 1), (2, 'English', 1), (3, 'Mathematics', 1), 
                (4, 'Mathematics', 3), (5, 'Physics', 3), (6, 'Chemistry', 3), 
                (7, 'General Studies', 2), 
                (8, 'Physics', 4), (9, 'Chemistry', 4), (10, 'Biology', 4), 
                (11, 'Mathematics', 5), (12, 'Physics', 5), (13, 'Chemistry', 5)
            ]
            cursor.executemany("INSERT INTO Subject (subject_id, subject_name, exam_id) VALUES (?, ?, ?)", subjects)
            
        conn.commit()
        print("Setup completed! You can now run 'add_questions.py' to populate questions.")
        
    except sqlite3.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

if __name__ == "__main__":
    setup()