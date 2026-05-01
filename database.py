import sqlite3
def init_db():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT
                   )            
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           student_id INTEGER,
            subject_name TEXT,
            marks REAL,
            FOREIGN KEY(student_id) REFERENCES students(id))
        """)
    conn.commit()
    conn.close()
init_db()
