"""
Database Configuration for TEST ARENA
"""
import sqlite3
import hashlib
import os

class Database:
    def __init__(self):
        """Initialize database connection parameters"""
        self.database = 'test_arena.db'
        self.connection = None
    
    def connect(self):
        """Create database connection"""
        try:
            self.connection = sqlite3.connect(self.database)
            self.connection.row_factory = sqlite3.Row  # Access columns by name
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a database query"""
        try:
            if not self.connection:
                self.connect()
                
            cursor = self.connection.cursor()
            
            # SQLite uses ? for placeholders, MySQL uses %s. 
            # We replace %s with ? to support existing queries.
            query = query.replace('%s', '?')
            
            cursor.execute(query, params or ())
            
            if fetch:
                result = [dict(row) for row in cursor.fetchall()]
                cursor.close()
                return result
            else:
                self.connection.commit()
                last_id = cursor.lastrowid
                cursor.close()
                return last_id
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # User Management Methods
    def create_user(self, name, username, password, email='', phone=''):
        """Create a new user account"""
        hashed_password = self.hash_password(password)
        query = """
            INSERT INTO User (name, username, password, email, phone)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (name, username, hashed_password, email, phone))
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        hashed_password = self.hash_password(password)
        query = """
            SELECT user_id, name, username FROM User 
            WHERE username = %s AND password = %s
        """
        result = self.execute_query(query, (username, hashed_password), fetch=True)
        return result[0] if result else None
    
    def check_username_exists(self, username):
        """Check if username already exists"""
        query = "SELECT user_id FROM User WHERE username = %s"
        result = self.execute_query(query, (username,), fetch=True)
        return len(result) > 0
    
    # Exam Methods
    def get_all_exams(self):
        """Get all available exams"""
        query = "SELECT * FROM Exam ORDER BY exam_name"
        return self.execute_query(query, fetch=True)
    
    def get_exam_by_id(self, exam_id):
        """Get exam details by ID"""
        query = "SELECT * FROM Exam WHERE exam_id = %s"
        result = self.execute_query(query, (exam_id,), fetch=True)
        return result[0] if result else None
    
    # Question Methods
    def get_questions_by_exam(self, exam_id):
        """Get all questions for an exam"""
        query = """
            SELECT q.*, s.subject_name 
            FROM Question q
            JOIN Subject s ON q.subject_id = s.subject_id
            WHERE q.exam_id = %s
            ORDER BY RANDOM()
        """
        # Note: RAND() in MySQL is RANDOM() in SQLite.
        # I need to handle this query specifically since replace('%s', '?') won't catch RAND()
        query = query.replace('RAND()', 'RANDOM()')
        
        return self.execute_query(query, (exam_id,), fetch=True)
    
    def get_subjects_by_exam(self, exam_id):
        """Get all subjects for an exam"""
        query = "SELECT * FROM Subject WHERE exam_id = %s"
        return self.execute_query(query, (exam_id,), fetch=True)
    
    # Score Methods
    def save_score(self, user_id, exam_id, mode, total_marks, correct, wrong, unanswered, time_taken):
        """Save quiz score"""
        # Get attempt number
        query = """
            SELECT COALESCE(MAX(attempt_number), 0) + 1 as next_attempt
            FROM Score WHERE user_id = %s AND exam_id = %s AND mode = %s
        """
        result = self.execute_query(query, (user_id, exam_id, mode), fetch=True)
        attempt_number = result[0]['next_attempt'] if result else 1
        
        # Insert score
        query = """
            INSERT INTO Score (user_id, exam_id, mode, attempt_number, total_marks, 
                             correct_answers, wrong_answers, unanswered, time_taken_minutes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self.execute_query(query, (user_id, exam_id, mode, attempt_number, 
                                         total_marks, correct, wrong, unanswered, time_taken))
    
    def get_user_scores(self, user_id):
        """Get all scores for a user"""
        query = """
            SELECT s.*, e.exam_name 
            FROM Score s
            JOIN Exam e ON s.exam_id = e.exam_id
            WHERE s.user_id = %s
            ORDER BY s.attempt_date DESC
        """
        # Note: SQLite stores dates as strings usually, but retrieval is same.
        # We might need to parse date string in python if it comes back as string.
        # However, for now, let's assume standard behavior.
        return self.execute_query(query, (user_id,), fetch=True)
    
    def get_user_best_scores(self, user_id):
        """Get best scores for each exam"""
        query = """
            SELECT e.exam_name, s.mode, MAX(s.total_marks) as best_score,
                   COUNT(*) as total_attempts
            FROM Score s
            JOIN Exam e ON s.exam_id = e.exam_id
            WHERE s.user_id = %s
            GROUP BY e.exam_name, s.mode
            ORDER BY e.exam_name, s.mode
        """
        return self.execute_query(query, (user_id,), fetch=True)
    
    def save_user_answer(self, score_id, question_id, selected_option, is_correct):
        """Save individual answer (optional detailed tracking)"""
        query = """
            INSERT INTO UserAnswer (score_id, question_id, selected_option, is_correct)
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (score_id, question_id, selected_option, is_correct))

