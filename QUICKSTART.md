# TEST ARENA - Quick Start Guide

## Quick Setup (5 Minutes)

### 1. Install MySQL
- Download and install MySQL Server from https://dev.mysql.com/downloads/
- Remember your root password

### 2. Install Python Package
```bash
pip install mysql-connector-python
```

### 3. Set Up Database
Open MySQL command line or MySQL Workbench and run:
```bash
mysql -u root -p < database_schema.sql
```

Or copy-paste the contents of `database_schema.sql` into MySQL Workbench and execute.

### 4. Configure Database Connection
Open `database.py` and update lines 9-10:
```python
self.user = 'root'              # Your MySQL username
self.password = 'your_password'  # Your MySQL password
```

### 5. Run the Application
```bash
python main.py
```

## First Login

1. Select option **2** (Sign Up)
2. Create your account
3. Login with your credentials
4. Start taking quizzes!

## Default Exam Settings

| Exam | Duration | Questions |
|------|----------|-----------|
| PSC  | 90 mins  | 100       |
| UPSC | 120 mins | 100       |
| KEAM | 150 mins | 100       |
| NEET | 180 mins | 100       |
| JEE  | 180 mins | 100       |

## Sample Questions Included

The database comes with sample questions for all exams:
- **PSC**: General Knowledge, Mathematics, Current Affairs
- **UPSC**: General Studies, History, Current Affairs
- **KEAM**: Mathematics, Physics, Chemistry
- **NEET**: Physics, Chemistry, Biology
- **JEE**: Mathematics, Physics, Chemistry

## Add More Questions

To add more sample questions:
```bash
python add_questions.py
mysql -u root -p test_arena < additional_questions.sql
```

## How to Use

### Exam Mode
- Realistic exam simulation
- Strict time limits
- No feedback during exam
- Results shown at end
- Best for: Final preparation

### Free Trial Mode
- Practice mode
- Immediate feedback
- View solutions
- No time pressure
- Best for: Learning and practice

## Tips

1. **Start with Free Trial** to familiarize yourself with questions
2. **Take Exam Mode** when you're ready for realistic practice
3. **Track your progress** in the Scores section
4. **Focus on weak subjects** by reviewing your performance

## Need Help?

- Check `README.md` for detailed documentation
- Database issues? Verify MySQL is running
- Connection errors? Check `database.py` credentials
- No questions? Run `database_schema.sql` again

## Project Files

- `main.py` - Main application
- `database.py` - Database operations
- `database_schema.sql` - Database structure + sample data
- `additional_questions.sql` - Extra questions
- `README.md` - Full documentation

Happy Learning! 🎓
