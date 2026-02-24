
import sqlite3
import os
from database import Database

# Base questions for other subjects
base_sql = """
-- Additional PSC Questions (General Knowledge)
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(1, 1, 'Who is known as the Father of Indian Constitution?', 'Mahatma Gandhi', 'Dr. B.R. Ambedkar', 'Jawaharlal Nehru', 'Sardar Patel', 'B', 'Dr. B.R. Ambedkar is known as the Father of the Indian Constitution.'),
(1, 1, 'Which is the largest state in India by area?', 'Maharashtra', 'Rajasthan', 'Madhya Pradesh', 'Uttar Pradesh', 'B', 'Rajasthan is the largest state in India by area.'),
(1, 1, 'The national song of India is?', 'Jana Gana Mana', 'Vande Mataram', 'Saare Jahan Se Achha', 'Maa Tujhe Salaam', 'B', 'Vande Mataram is the national song of India.'),
(1, 1, 'Which river is called the Sorrow of Bihar?', 'Ganga', 'Kosi', 'Brahmaputra', 'Yamuna', 'B', 'River Kosi is called the Sorrow of Bihar due to frequent flooding.'),
(1, 1, 'The headquarters of Reserve Bank of India is in?', 'New Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'B', 'RBI headquarters is located in Mumbai.');

-- PSC Mathematics Questions
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(1, 3, 'What is the square root of 144?', '10', '11', '12', '13', 'C', 'Square root of 144 is 12 (12 × 12 = 144).'),
(1, 3, 'What is 20% of 500?', '50', '75', '100', '125', 'C', '20% of 500 = (20/100) × 500 = 100.'),
(1, 3, 'If x + 5 = 12, what is x?', '5', '6', '7', '8', 'C', 'x + 5 = 12, therefore x = 12 - 5 = 7.'),
(1, 3, 'What is the value of 5³?', '15', '25', '75', '125', 'D', '5³ = 5 × 5 × 5 = 125.');

-- NEET Chemistry Questions
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(4, 9, 'What is the atomic number of Carbon?', '4', '5', '6', '7', 'C', 'Carbon has atomic number 6.'),
(4, 9, 'The chemical formula of water is?', 'H₂O', 'HO₂', 'H₃O', 'HO', 'A', 'Water has the chemical formula H₂O.'),
(4, 9, 'Which gas is most abundant in Earth''s atmosphere?', 'Oxygen', 'Nitrogen', 'Carbon dioxide', 'Argon', 'B', 'Nitrogen makes up about 78% of Earth''s atmosphere.'),
(4, 9, 'The pH of pure water is?', '5', '6', '7', '8', 'C', 'Pure water has a pH of 7, which is neutral.');

-- NEET Biology Questions
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(4, 10, 'Which organ is responsible for pumping blood?', 'Liver', 'Heart', 'Kidney', 'Lungs', 'B', 'The heart is responsible for pumping blood throughout the body.'),
(4, 10, 'What is the basic unit of life?', 'Tissue', 'Organ', 'Cell', 'Molecule', 'C', 'The cell is the basic structural and functional unit of life.'),
(4, 10, 'DNA stands for?', 'Deoxyribonucleic Acid', 'Diribonucleic Acid', 'Dexyribose Acid', 'Deoxyribose Nucleic', 'A', 'DNA stands for Deoxyribonucleic Acid.'),
(4, 10, 'Which vitamin is known as ascorbic acid?', 'Vitamin A', 'Vitamin B', 'Vitamin C', 'Vitamin D', 'C', 'Vitamin C is also known as ascorbic acid.'),
(4, 10, 'How many chambers does the human heart have?', 'Two', 'Three', 'Four', 'Five', 'C', 'The human heart has four chambers: two atria and two ventricles.'),
(4, 10, 'Which is the largest organ in the human body?', 'Liver', 'Brain', 'Skin', 'Heart', 'C', 'The skin is the largest organ in the human body.');

-- JEE Mathematics Questions
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(5, 11, 'What is the derivative of x²?', 'x', '2x', 'x²', '2', 'B', 'd/dx(x²) = 2x'),
(5, 11, 'What is the value of sin 90°?', '0', '0.5', '1', '∞', 'C', 'sin 90° = 1'),
(5, 11, 'The area of a circle with radius r is?', 'πr', 'πr²', '2πr', 'πd', 'B', 'Area of circle = πr²');

-- JEE Chemistry Questions
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(5, 13, 'What is Avogadro''s number?', '6.022 × 10²¹', '6.022 × 10²²', '6.022 × 10²³', '6.022 × 10²⁴', 'C', 'Avogadro''s number is 6.022 × 10²³ mol⁻¹'),
(5, 13, 'The chemical symbol for Gold is?', 'Go', 'Gd', 'Au', 'Ag', 'C', 'Au is the chemical symbol for Gold (from Latin: Aurum).');

-- KEAM Mathematics Questions
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(3, 4, 'What is the value of π (pi) approximately?', '3.14', '3.41', '2.14', '4.13', 'A', 'The value of π is approximately 3.14159...'),
(3, 4, 'What is 10!/(8!×2!)?', '40', '45', '50', '55', 'B', '10!/(8!×2!) = (10×9)/(2×1) = 45');

-- KEAM Chemistry Questions
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(3, 6, 'What is the molecular formula of glucose?', 'C₆H₁₂O₆', 'C₅H₁₂O₆', 'C₆H₁₀O₆', 'C₆H₁₂O₅', 'A', 'Glucose has the molecular formula C₆H₁₂O₆'),
(3, 6, 'What is the valency of Calcium?', '1', '2', '3', '4', 'B', 'Calcium has a valency of 2.');

-- UPSC Questions
INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) VALUES
(2, 4, 'When was the Indian Independence Act passed?', '1945', '1946', '1947', '1948', 'C', 'The Indian Independence Act was passed in 1947.'),
(2, 4, 'Who was the first woman Prime Minister of India?', 'Sarojini Naidu', 'Indira Gandhi', 'Pratibha Patil', 'Sonia Gandhi', 'B', 'Indira Gandhi was the first woman Prime Minister of India.'),
(2, 4, 'The Battle of Plassey was fought in?', '1757', '1764', '1857', '1947', 'A', 'The Battle of Plassey was fought in 1757.');
"""

# New Math Questions (Relations & Functions)
math_questions = [
    ('Let R be a relation on the set R of all real numbers defined by aRb iff |a| <= b. Then the relation R is:', 'Reflexive', 'Symmetric', 'Transitive', 'Equivalence', 'C', 'For transitivity: If |a| <= b and |b| <= c. Since |a| <= b implies b >= 0, so |b| = b. Thus |a| <= b <= c implies |a| <= c.'),
    ('If f: [0, ∞) -> [0, ∞) defined by f(x) = x² is onto, then the interval of x is:', '[0, ∞)', '(-∞, 0]', '(-∞, ∞)', '[1, ∞)', 'A', 'The range of f(x) = x² for domain [0, ∞) is [0, ∞). Since it is onto, the codomain matches the range.'),
    ('The domain of the function f(x) = sin⁻¹(x-3) is:', '[0, 1]', '[0, 2]', '[2, 4]', '[3, 5]', 'C', '-1 <= x-3 <= 1 => 2 <= x <= 4.'),
    ('Let R be an equivalence relation on a finite set A having n elements. Then the number of ordered pairs in R is:', 'Less than n', 'Greater than or equal to n', 'Less than or equal to n', 'None of these', 'B', 'Since R is reflexive, it must contain (a,a) for all a in A. Thus it contains at least n pairs.'),
    ('The inverse of the function f(x) = (e^x - e^-x)/(e^x + e^-x) + 2 is:', 'log((x-2)/(x-1))', '0.5 log((x-1)/(3-x))', 'log((x-1)/(x+1))', 'None of these', 'B', 'Let y = f(x). y-2 = tanh(x). x = arctanh(y-2) = 0.5 log((1+(y-2))/(1-(y-2))) = 0.5 log((y-1)/(3-y)).'),
    ('If f(x) = log((1+x)/(1-x)) and g(x) = (3x+x^3)/(1+3x^2), then f(g(x)) is:', '3f(x)', '(f(x))^3', 'f(3x)', 'None of these', 'A', 'f(g(x)) = log((1+g)/(1-g)). (1+g)/(1-g) = ((1+x)^3)/((1-x)^3). So f(g(x)) = 3 log((1+x)/(1-x)) = 3f(x).'),
    ('A relation R on the set of natural numbers is defined by x is a factor of y. The relation is:', 'Reflexive and symmetric', 'Transitive and symmetric', 'Equivalence', 'Reflexive, transitive but not symmetric', 'D', 'Reflexive (x|x), Transitive (x|y, y|z -> x|z), Not Symmetric (2|4 but 4 does not divide 2).'),
    ('Let f(x) = cos(log x). Then f(x)f(y) - 0.5[f(x/y)+f(xy)] is:', '0', '1', '-1', 'None of these', 'A', 'cos(A)cos(B) - 0.5[cos(A-B) + cos(A+B)] = 0.'),
    ('Let A = {1, 2, 3}. The number of equivalence relations containing (1, 2) is:', '1', '2', '3', '4', 'B', 'Relations are {(1,1),(2,2),(3,3),(1,2),(2,1)} and {(1,1),(2,2),(3,3),(1,2),(2,1),(1,3),(3,1),(2,3),(3,2)}. Total 2.'),
    ('If f(x) = (x-1)/(x+1), then f(2x) is equal to:', 'f(x)+1', '(3f(x)+1)/(f(x)+3)', '(f(x)+3)/(3f(x)+1)', 'None of these', 'B', 'Substitute f(x) into the expression to verify.')
]

# New Physics Questions (Electrostatics)
physics_questions = [
    ('The existence of a negative charge on a body implies that it has:', 'Lost some of its electrons', 'Lost some of its protons', 'Acquired some electrons from outside', 'Acquired some protons from outside', 'C', 'Negatively charged bodies have an excess of electrons.'),
    ('Three equal charges q are placed at the corners of an equilateral triangle of side a. The force on any charge is:', 'Zero', '√3 q² / (4πε₀a²)', 'q² / (4πε₀a²)', '2q² / (4πε₀a²)', 'B', 'Resultant of two forces F at 60 degrees is √3 F.'),
    ('The electric field due to a point charge is proportional to:', 'r', 'r⁻¹', 'r⁻²', 'r⁻³', 'C', 'E = kQ/r².'),
    ('When an electric dipole is placed in a uniform electric field, the moment of couple (torque) is maximum when the dipole is placed:', 'Along the field', 'Perpendicular to the field', 'At 45° to the field', 'Opposite to the field', 'B', 'Torque τ = pE sin θ. Max at θ = 90°.'),
    ('SI unit of electric flux is:', 'Weber', 'Volt meter', 'Volt / meter', 'Newton / Coulomb', 'B', 'Flux Φ = E.A = (V/m) * m² = V m.'),
    ('The total positive charge in a glass of water containing 360g of water is approximately:', '1.9 × 10⁷ C', '1.9 × 10⁶ C', '1.9 × 10⁵ C', '1.9 × 10⁴ C', 'A', '360g H2O = 20 mol. Protons = 20 * 6.02e23 * 10. Charge = 1.2e26 * 1.6e-19 ≈ 1.92e7 C.'),
    ('If the distance between two point charges is halved, the electrical force between them becomes:', '2 times', '4 times', '1/2 times', '1/4 times', 'B', 'F ∝ 1/r². If r becomes r/2, F becomes 4F.'),
    ('A cube of side a has point charges +q at each vertex except one origin where it is -q. The electric field at the center is:', '-2q / (3πε₀a²) along diagonal', '2q / (3πε₀a²) along diagonal', '-q / (3πε₀a²) along diagonal', 'None', 'B', 'Equivalent to 8 +q charges (E=0) and a -2q charge at origin. Field due to -2q at origin points towards origin (along diagonal). Magnitude E = k(2q)/r² where r=√3a/2.'),
    ('A spherical conductor of radius 10 cm has a charge of 3.2 × 10⁻⁷ C. Magnitude of electric field at 15 cm from center is:', '1.28 × 10⁵ N/C', '1.28 × 10⁴ N/C', '1.28 × 10⁶ N/C', '1.28 × 10⁷ N/C', 'A', 'E = kQ/r² = 9e9 * 3.2e-7 / (0.15)².'),
    ('Polar molecules are those:', 'Having permanent electric dipole moment', 'Having zero dipole moment', 'Acquire dipole moment only in field', 'None', 'A', 'Polar molecules have permanent dipole moments.')
]

# New Chemistry Questions (Solutions)
chemistry_questions = [
    ('The value of Henry’s constant KH is:', 'Greater for gases with higher solubility', 'Greater for gases with lower solubility', 'Constant for all gases', 'Not related to solubility', 'B', 'p = KH * x. For same p, higher KH means lower x (solubility).'),
    ('Which concentration unit is independent of temperature?', 'Molarity', 'Normality', 'Molality', 'Formality', 'C', 'Molality depends on mass, which is independent of temperature.'),
    ('The boiling point of a solution containing 18g of substance in 100g of solvent is 100.52°C. If Kb=0.52 and Kf=1.86, the freezing point will be:', '-0.52°C', '-1.86°C', '-3.72°C', '-0.93°C', 'B', 'ΔTb = 0.52 => m = 1. ΔTf = Kf * m = 1.86. Tf = -1.86°C.'),
    ('An unripe mango shrivels when placed in a concentrated salt solution due to:', 'Osmosis', 'Reverse Osmosis', 'Diffusion', 'Vaporization', 'A', 'Water moves out of the mango (hypotonic) to the salt solution (hypertonic).'),
    ('Low blood oxygen in people at high altitudes is due to:', 'High atmospheric pressure', 'Low atmospheric pressure', 'High temperature', 'Low temperature', 'B', 'Partial pressure of oxygen is lower at high altitudes.'),
    ('Which of the following is an ideal solution?', 'Ethanol + Acetone', 'Benzene + Toluene', 'Chloroform + Acetone', 'Phenol + Aniline', 'B', 'Benzene and Toluene form an ideal solution.'),
    ('The van\'t Hoff factor i for SrCl2 solution is 2.74. The degree of dissociation is:', '91.3%', '87%', '100%', '74%', 'B', 'i = 1 + (n-1)α. 2.74 = 1 + 2α => α = 0.87.'),
    ('Mole fraction of solvent in aqueous solution of solute is 0.8. The molality is:', '13.88', '13.88 x 10^-3', '13.88', '13.88 x 10^-2', 'A', 'm = (0.2 * 1000) / (0.8 * 18) = 13.88.'),
    ('The normality of 1.5 M H3PO4 is:', '1.5 N', '3 N', '4.5 N', '6 N', 'C', 'Normality = Molarity * n-factor. n=3 for H3PO4. N = 1.5 * 3 = 4.5.'),
    ('Blood cells are isotonic with:', '0.9% (w/v) NaCl', '0.9% (w/v) KCl', 'Pure water', '1.5% (w/v) NaCl', 'A', '0.9% NaCl solution is isotonic with blood plasma.')
]

# GK questions to be added to PSC
gk_questions = [
    ('Who is known as the Father of the Indian Constitution?', 'Mahatma Gandhi', 'Dr. B.R. Ambedkar', 'Jawaharlal Nehru', 'Sardar Patel', 'B', 'Dr. B.R. Ambedkar was the chairman of the Drafting Committee and is known as the Father of the Indian Constitution.'),
    ('Which is the largest state in India by area?', 'Maharashtra', 'Rajasthan', 'Madhya Pradesh', 'Uttar Pradesh', 'B', 'Rajasthan is the largest state in India, covering about 10.4% of the total geographical area.'),
    ('The national song of India is:', 'Jana Gana Mana', 'Vande Mataram', 'Saare Jahan Se Achha', 'Maa Tujhe Salaam', 'B', 'Vande Mataram, composed in Sanskrit by Bankimchandra Chatterji, is the national song of India.'),
    ('Which river is called the "Sorrow of Bihar"?', 'Ganga', 'Kosi', 'Brahmaputra', 'Yamuna', 'B', 'The Kosi River is known as the Sorrow of Bihar due to its frequent and devastating floods.'),
    ('The headquarters of the Reserve Bank of India (RBI) is in:', 'New Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'B', 'The RBI headquarters was permanently moved from Kolkata to Mumbai in 1937.'),
    ('Who was the first President of India?', 'Dr. Rajendra Prasad', 'Dr. S. Radhakrishnan', 'Dr. Zakir Hussain', 'V.V. Giri', 'A', 'Dr. Rajendra Prasad served as the first President of India from 1950 to 1962.'),
    ('What is the capital of Kerala?', 'Kochi', 'Thiruvananthapuram', 'Kozhikode', 'Thrissur', 'B', 'Thiruvananthapuram is the capital and largest city of the Indian state of Kerala.'),
    ('When was the Indian Independence Act passed?', '1945', '1946', '1947', '1948', 'C', 'The Indian Independence Act was passed by the Parliament of the United Kingdom in 1947.'),
    ('Who was the first woman Prime Minister of India?', 'Sarojini Naidu', 'Indira Gandhi', 'Pratibha Patil', 'Sonia Gandhi', 'B', 'Indira Gandhi served as the first and, to date, only female Prime Minister of India.'),
    ('The Battle of Plassey was fought in:', '1757', '1764', '1857', '1947', 'A', 'This battle took place on June 23, 1757, between the British East India Company and the Nawab of Bengal.'),
    ('Which vitamin is known as ascorbic acid?', 'Vitamin A', 'Vitamin B', 'Vitamin C', 'Vitamin D', 'C', 'Vitamin C is essential for the repair of all body tissues and is known as ascorbic acid.'),
    ('What is the basic unit of life?', 'Tissue', 'Organ', 'Cell', 'Molecule', 'C', 'The cell is the basic structural, functional, and biological unit of all known organisms.'),
    ('DNA stands for:', 'Deoxyribonucleic Acid', 'Diribonucleic Acid', 'Dexyribose Acid', 'Deoxyribose Nucleic', 'A', 'DNA is a molecule that carries genetic instructions in all known living organisms.'),
    ('How many chambers does the human heart have?', 'Two', 'Three', 'Four', 'Five', 'C', 'The human heart consists of four chambers: two atria and two ventricles.'),
    ('Which is the largest organ in the human body?', 'Liver', 'Brain', 'Skin', 'Heart', 'C', 'The skin is the largest organ of the body, covering the entire external surface.'),
    ('The speed of light in vacuum is approximately:', '3 × 10⁶ m/s', '3 × 10⁷ m/s', '3 × 10⁸ m/s', '3 × 10⁹ m/s', 'C', 'Light travels at a speed of approximately 299,792,458 meters per second in a vacuum.'),
    ('The SI unit of force is:', 'Pascal', 'Newton', 'Joule', 'Watt', 'B', 'Named after Isaac Newton, the Newton (N) is the derived unit of force.'),
    ('What type of lens is used to correct myopia (short-sightedness)?', 'Convex', 'Concave', 'Bifocal', 'Cylindrical', 'B', 'A concave lens diverges light rays before they reach the eye to correct myopia.'),
    ('Which gas is most abundant in Earth\'s atmosphere?', 'Oxygen', 'Nitrogen', 'Carbon dioxide', 'Argon', 'B', 'Nitrogen makes up approximately 78% of Earth\'s atmosphere.'),
    ('What is the atomic number of Carbon?', '4', '5', '6', '7', 'C', 'Carbon has 6 protons in its nucleus, making its atomic number 6.'),
    ('The pH of pure water is:', '5', '6', '7', '8', 'C', 'Pure water is neutral on the pH scale with a value of 7.'),
    ('Which organ is responsible for pumping blood?', 'Liver', 'Heart', 'Kidney', 'Lungs', 'B', 'The heart acts as a pump to circulate blood through the body\'s blood vessels.'),
    ('What is the square root of 144?', '10', '11', '12', '13', 'C', '12 × 12 = 144.'),
    ('What is 20% of 500?', '50', '75', '100', '125', 'C', '(20/100) × 500 = 100.'),
    ('If x + 5 = 12, what is x?', '5', '6', '7', '8', 'C', 'x = 12 - 5 = 7.')
]

# Target exams: KEAM (3, 5), NEET (4, 8), JEE (5, 12)
# Physics targets
physics_target_exams = [
    (3, 5, 'KEAM'),
    (4, 8, 'NEET'),
    (5, 12, 'JEE')
]

# Target exams for Chemistry: KEAM (3, 6), NEET (4, 9), JEE (5, 13)
chem_target_exams = [
    (3, 6, 'KEAM'),
    (4, 9, 'NEET'),
    (5, 13, 'JEE')
]

# Math targets: KEAM (3, 4), JEE (5, 11)
math_target_exams = [
    (3, 4, 'KEAM'),
    (5, 11, 'JEE')
]

# Target exams for GK: PSC (1, 1)
gk_target_exams = [
    (1, 1, 'PSC')
]

# New UPSC Questions
upsc_questions = [
    ('Consider the following infrastructure sectors:\n1.Affordable housing\n2.Mass rapid transport\n3.Health care\n4.Renewable energy\nOn how many of the above does the UNOPS Sustainable Investments in Infrastructure and Innovation (S3I) initiative focus for its investments?', 'Only one', 'Only two', 'Only three', 'All four', 'C', 'Explanation: The S3I initiative specifically focuses on three sectors: Affordable Housing, Renewable Energy, and Health Infrastructure.\n\nTrend Note: This reflects the recent UPSC shift toward "Only one/two/three" style options, which makes traditional elimination techniques much harder.')
]

# Target exams for UPSC: General Studies (2, 7)
upsc_target_exams = [
    (2, 7, 'UPSC')
]

def add_questions_to_db():
    print("Connecting to database (SQLite)...")
    db_config = Database()
    
    if not os.path.exists(db_config.database):
        print("Database not found. Please run setup_database.py first.")
        return

    try:
        conn = sqlite3.connect(db_config.database)
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("Inserting base questions...")
        # Execute base_sql (multiple statements) - use executescript for multiple statements
        cursor.executescript(base_sql)
            
        print("Inserting additional subject questions...")
        
        insert_query = """
        INSERT INTO Question (exam_id, subject_id, question_text, option_a, option_b, option_c, option_d, correct_option, solution) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Helper to insert questions
        def insert_list(target_exams, questions):
            for exam_id, subject_id, exam_name in target_exams:
                data_to_insert = []
                for q in questions:
                    # q structure: (text, opt_a, opt_b, opt_c, opt_d, correct, solution)
                    # We need to prepend exam_id and subject_id
                    row = (exam_id, subject_id) + q
                    data_to_insert.append(row)
                
                if data_to_insert:
                    cursor.executemany(insert_query, data_to_insert)
                    print(f"Added {len(data_to_insert)} questions for {exam_name}")

        # Insert for each category
        insert_list(physics_target_exams, physics_questions)
        insert_list(chem_target_exams, chemistry_questions)
        insert_list(math_target_exams, math_questions)
        insert_list(gk_target_exams, gk_questions)
        insert_list(upsc_target_exams, upsc_questions)
        
        conn.commit()
        print("All questions inserted successfully!")
        cursor.close()
        conn.close()
        
    except sqlite3.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    add_questions_to_db()
