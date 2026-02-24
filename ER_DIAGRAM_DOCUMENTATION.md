# TEST ARENA - Database ER Diagram Documentation

## Entity-Relationship Diagram

### Entities and Relationships

```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ PK: user_id     │
│    name         │
│    username     │
│    password     │
│    email        │
│    created_at   │
└────────┬────────┘
         │
         │ 1:N (has many)
         │
         ▼
┌─────────────────┐
│     SCORES      │
├─────────────────┤
│ PK: score_id    │
│ FK: user_id     │◄───────┐
│ FK: exam_id     │        │
│    mode         │        │
│    attempt_num  │        │
│    total_marks  │        │
│    correct_ans  │        │
│    wrong_ans    │        │
│    time_taken   │        │
│    attempted_at │        │
└─────────────────┘        │
         ▲                 │
         │                 │
         │ N:1 (belongs to)│
         │                 │
┌────────┴────────┐        │
│     EXAMS       │        │
├─────────────────┤        │
│ PK: exam_id     │        │
│    exam_name    │        │
│    total_ques   │        │
│    time_limit   │        │
│    description  │        │
└────────┬────────┘        │
         │                 │
         │ 1:N (has many)  │
         │                 │
         ▼                 │
┌─────────────────┐        │
│    SUBJECTS     │        │
├─────────────────┤        │
│ PK: subject_id  │        │
│ FK: exam_id     │        │
│    subject_name │        │
│    ques_count   │        │
└────────┬────────┘        │
         │                 │
         │ 1:N (has many)  │
         │                 │
         ▼                 │
┌─────────────────┐        │
│   QUESTIONS     │        │
├─────────────────┤        │
│ PK: question_id │        │
│ FK: exam_id     │────────┘
│ FK: subject_id  │
│    question_txt │
│    option_a     │
│    option_b     │
│    option_c     │
│    option_d     │
│    correct_opt  │
│    solution     │
└─────────────────┘
```

## Relationships Explained

### 1. Users ↔ Scores (1:N)
- **Relationship**: One user can have multiple score records
- **Cardinality**: 1:N (One-to-Many)
- **Foreign Key**: Scores.user_id → Users.user_id
- **Description**: Each user can attempt multiple quizzes, creating multiple score entries

### 2. Exams ↔ Scores (1:N)
- **Relationship**: One exam can have multiple score records
- **Cardinality**: 1:N (One-to-Many)
- **Foreign Key**: Scores.exam_id → Exams.exam_id
- **Description**: Each exam can be attempted by multiple users multiple times

### 3. Exams ↔ Subjects (1:N)
- **Relationship**: One exam has multiple subjects
- **Cardinality**: 1:N (One-to-Many)
- **Foreign Key**: Subjects.exam_id → Exams.exam_id
- **Description**: Each exam consists of multiple subjects (e.g., NEET has Biology, Physics, Chemistry)

### 4. Subjects ↔ Questions (1:N)
- **Relationship**: One subject has multiple questions
- **Cardinality**: 1:N (One-to-Many)
- **Foreign Key**: Questions.subject_id → Subjects.subject_id
- **Description**: Each subject contains multiple questions

### 5. Exams ↔ Questions (1:N)
- **Relationship**: One exam has multiple questions
- **Cardinality**: 1:N (One-to-Many)
- **Foreign Key**: Questions.exam_id → Exams.exam_id
- **Description**: Each exam has a set of questions distributed across subjects

## Detailed Entity Descriptions

### USERS Entity
**Purpose**: Store user account information

| Attribute   | Type      | Constraints           | Description                    |
|-------------|-----------|----------------------|--------------------------------|
| user_id     | INTEGER   | PRIMARY KEY, AUTO    | Unique identifier for user     |
| name        | TEXT      | NOT NULL             | Full name of user              |
| username    | TEXT      | UNIQUE, NOT NULL     | Login username                 |
| password    | TEXT      | NOT NULL             | Hashed password (SHA-256)      |
| email       | TEXT      | -                    | Email address (optional)       |
| created_at  | TIMESTAMP | DEFAULT NOW          | Account creation timestamp     |

### EXAMS Entity
**Purpose**: Store exam category information

| Attribute       | Type    | Constraints        | Description                    |
|-----------------|---------|-------------------|--------------------------------|
| exam_id         | INTEGER | PRIMARY KEY, AUTO | Unique identifier for exam     |
| exam_name       | TEXT    | UNIQUE, NOT NULL  | Name (PSC, UPSC, etc.)        |
| total_questions | INTEGER | NOT NULL          | Total questions in exam        |
| time_limit      | INTEGER | NOT NULL          | Time limit in minutes          |
| description     | TEXT    | -                 | Exam description               |

### SUBJECTS Entity
**Purpose**: Store subject information for each exam

| Attribute      | Type    | Constraints           | Description                    |
|----------------|---------|----------------------|--------------------------------|
| subject_id     | INTEGER | PRIMARY KEY, AUTO    | Unique identifier for subject  |
| subject_name   | TEXT    | NOT NULL             | Subject name                   |
| exam_id        | INTEGER | FOREIGN KEY          | Reference to parent exam       |
| question_count | INTEGER | -                    | Number of questions            |

### QUESTIONS Entity
**Purpose**: Store quiz questions and answers

| Attribute     | Type    | Constraints           | Description                    |
|---------------|---------|----------------------|--------------------------------|
| question_id   | INTEGER | PRIMARY KEY, AUTO    | Unique identifier for question |
| exam_id       | INTEGER | FOREIGN KEY, NOT NULL| Reference to exam              |
| subject_id    | INTEGER | FOREIGN KEY, NOT NULL| Reference to subject           |
| question_text | TEXT    | NOT NULL             | The question                   |
| option_a      | TEXT    | NOT NULL             | First option                   |
| option_b      | TEXT    | NOT NULL             | Second option                  |
| option_c      | TEXT    | NOT NULL             | Third option                   |
| option_d      | TEXT    | NOT NULL             | Fourth option                  |
| correct_option| TEXT    | NOT NULL             | Correct answer (A/B/C/D)       |
| solution      | TEXT    | -                    | Explanation of answer          |

### SCORES Entity
**Purpose**: Store user quiz attempt results

| Attribute       | Type      | Constraints           | Description                    |
|-----------------|-----------|----------------------|--------------------------------|
| score_id        | INTEGER   | PRIMARY KEY, AUTO    | Unique identifier for score    |
| user_id         | INTEGER   | FOREIGN KEY, NOT NULL| Reference to user              |
| exam_id         | INTEGER   | FOREIGN KEY, NOT NULL| Reference to exam              |
| mode            | TEXT      | CHECK constraint     | 'Exam' or 'Free Trial'         |
| attempt_number  | INTEGER   | NOT NULL             | Attempt count for user/exam    |
| total_marks     | INTEGER   | NOT NULL             | Final score                    |
| correct_answers | INTEGER   | NOT NULL             | Number of correct answers      |
| wrong_answers   | INTEGER   | NOT NULL             | Number of wrong answers        |
| time_taken      | INTEGER   | -                    | Time in seconds                |
| attempted_at    | TIMESTAMP | DEFAULT NOW          | Timestamp of attempt           |

## Constraints and Integrity

### Primary Keys
- All tables have auto-incrementing integer primary keys
- Ensures unique identification of each record

### Foreign Keys
- **Scores.user_id** → Users.user_id
- **Scores.exam_id** → Exams.exam_id
- **Subjects.exam_id** → Exams.exam_id
- **Questions.exam_id** → Exams.exam_id
- **Questions.subject_id** → Subjects.subject_id

### Unique Constraints
- Users.username (prevents duplicate usernames)
- Exams.exam_name (prevents duplicate exam names)

### Check Constraints
- Scores.mode must be either 'Exam' or 'Free Trial'

### Not Null Constraints
- Applied to essential fields to ensure data completeness

## Sample Data Flow

### User Registration Flow
1. User enters details on signup page
2. Password is hashed using SHA-256
3. Data inserted into Users table
4. user_id generated automatically

### Quiz Attempt Flow
1. User selects exam → Queries Exams table
2. System loads subjects → Queries Subjects table
3. System loads questions → Queries Questions table
4. User answers questions → Stored in memory
5. Quiz completed → Calculate score
6. Save to Scores table with user_id, exam_id, and results

### Score Retrieval Flow
1. User requests score history
2. Query Scores table with user_id
3. JOIN with Exams table to get exam names
4. Display results with statistics

## Database Normalization

The database follows **Third Normal Form (3NF)**:

1. **First Normal Form (1NF)**
   - All attributes contain atomic values
   - No repeating groups

2. **Second Normal Form (2NF)**
   - All non-key attributes fully depend on primary key
   - No partial dependencies

3. **Third Normal Form (3NF)**
   - No transitive dependencies
   - All attributes depend only on primary key

## Query Examples

### Get all questions for an exam
```sql
SELECT q.question_text, q.option_a, q.option_b, q.option_c, q.option_d,
       s.subject_name
FROM Questions q
JOIN Subjects s ON q.subject_id = s.subject_id
WHERE q.exam_id = ?
```

### Get user's score history
```sql
SELECT e.exam_name, s.mode, s.total_marks, s.attempted_at
FROM Scores s
JOIN Exams e ON s.exam_id = e.exam_id
WHERE s.user_id = ?
ORDER BY s.attempted_at DESC
```

### Get average score per exam
```sql
SELECT e.exam_name, AVG(s.total_marks) as avg_score
FROM Scores s
JOIN Exams e ON s.exam_id = e.exam_id
GROUP BY e.exam_name
```

## Indexing Strategy

Recommended indexes for performance:
- Users.username (for login queries)
- Scores.user_id (for score retrieval)
- Questions.exam_id (for question loading)
- Questions.subject_id (for subject-wise queries)

---

This ER diagram and documentation provides a complete overview of the TEST ARENA database structure.
