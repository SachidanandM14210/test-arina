# Test_Arena
TEST ARENA - Quiz Application
A comprehensive quiz application for competitive exam preparation (PSC, UPSC, KEAM, NEET, JEE) built with Python and MySQL.
Features

User Authentication: Secure login and signup system with password hashing
Multiple Exams: Support for PSC, UPSC, KEAM, NEET, and JEE
Two Quiz Modes:

Exam Mode: Timed tests with no immediate feedback (realistic exam experience)
Free Trial Mode: Practice mode with instant feedback and solutions


Subject-wise Questions: Questions organized by subject areas
Score Tracking: Complete history of all attempts with best scores
Database-driven: All data stored securely in MySQL database

Technology Stack

Language: Python 3.x
Database: MySQL 8.0+
Libraries: mysql-connector-python

Database Schema
Tables:

User - Stores user account information
Exam - Contains exam details (name, duration, question count)
Subject - Subject information for each exam
Question - Quiz questions with options and solutions
Score - User attempt history and scores
UserAnswer - Optional detailed answer tracking

Installation
Prerequisites

Python 3.7 or higher
MySQL Server 8.0 or higher
pip (Python package manager)

Step 1: Install Required Python Packages
bashpip install mysql-connector-python
Step 2: Set Up MySQL Database

Start MySQL server
Login to MySQL:

bashmysql -u root -p

Create the database and tables:

bashmysql -u root -p < database_schema.sql
Or manually run the SQL commands from database_schema.sql
Step 3: Configure Database Connection
Edit database.py and update the database credentials:
pythonself.host = 'localhost'
self.database = 'test_arena'
self.user = 'root'          # Your MySQL username
self.password = 'your_password'  # Your MySQL password
Step 4: Add More Questions (Optional)
Run the question insertion script:
bashpython add_questions.py
This will create additional_questions.sql. Run it in MySQL:
bashmysql -u root -p test_arena < additional_questions.sql
Running the Application
bashpython main.py
Usage Guide
First Time User

Sign Up

Choose option 2 from the login menu
Enter your full name, username, and password
Optionally provide email and phone number


Login

Use your username and password to login


Start Quiz

Select from available exams (PSC, UPSC, KEAM, NEET, JEE)
Choose mode:

Exam Mode: Complete exam with time limit, results shown at end
Free Trial: Practice with immediate feedback after each question




View Scores

See all your previous attempts
View best scores for each exam



Exam Mode

Fixed time limit (varies by exam)
100 questions per exam
No indication of correct/wrong during exam
Final score displayed at the end
Score includes: correct answers, wrong answers, unanswered questions

Free Trial Mode

Practice without time pressure
Immediate feedback after each answer
Solution/explanation shown for each question
Still tracks score and time

Project Structure
test-arena/
│
├── main.py                 # Main application file
├── database.py             # Database connection and operations
├── database_schema.sql     # Database creation script
├── add_questions.py        # Script to generate more questions
├── additional_questions.sql # Additional sample questions
└── README.md              # This file
Database ER Diagram (Conceptual)
User (1) ----< (M) Score (M) >---- (1) Exam
                     |
                     | (1)
                     |
                    (M)
                UserAnswer (M) >---- (1) Question (M) >---- (1) Subject
                                                |
                                                | (M)
                                                |
                                               (1)
                                              Exam
Key Relationships

One User can have multiple Scores
One Exam can have multiple Scores
One Exam has multiple Subjects
One Subject has multiple Questions
One Score can have multiple UserAnswers
One Question can have multiple UserAnswers

Adding Your Own Questions
You can add questions directly to the database:
sqlINSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, 
                     option_c, option_d, correct_option, solution) 
VALUES (
    1,  -- exam_id (1=PSC, 2=UPSC, 3=KEAM, 4=NEET, 5=JEE)
    1,  -- subject_id (check Subject table for IDs)
    'Your question text?',
    'Option A',
    'Option B',
    'Option C',
    'Option D',
    'B',  -- Correct option (A/B/C/D)
    'Explanation of the answer'
);
Security Features

Passwords are hashed using SHA-256
SQL injection prevention through parameterized queries
Username uniqueness validation

Future Enhancements

 GUI using Tkinter or PyQt
 Question difficulty levels
 Performance analytics and graphs
 Export scores to PDF
 Admin panel for question management
 Negative marking option
 Question bookmarking
 Review answers after exam
 Leaderboard system

Troubleshooting
Common Issues

Database Connection Error

Ensure MySQL server is running
Check username and password in database.py
Verify database name is correct


No Questions Available

Run database_schema.sql to create sample questions
Add more questions using add_questions.py


Module Not Found Error

Install required packages: pip install mysql-connector-python



Contributing
This is a DBMS project. Feel free to fork and enhance!
To Contribute:

Add more questions to different exams
Improve the UI/UX
Add new features
Fix bugs

License
This project is created for educational purposes as a DBMS project.
Contact
For issues or questions, please create an issue in the repository.

Version: 1.0
Created: 2025
Project Type: DBMS Academic Project
