from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)
def get_db():
    conn = sqlite3.connect("student.db")
    conn.row_factory = sqlite3.Row
    return conn
def calculate_gpa(marks):
    if marks >= 90:
        return 4.0, "A"
    elif marks >= 80:
        return 3.7, "A-"
    elif marks >= 70:
        return 3.3, "B+"
    elif marks >= 60:
        return 3.0, "B"
    elif marks >= 50:
        return 2.0, "C"
    elif marks >= 40:
        return 1.0, "D"
    else:
        return 0.0, "F" 
@app.route("/")
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    conn.close()
    return render_template("home.html", students=students)
@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO student(name) VALUES(?)", (name,))
        student_id = cursor.lastrowid
        
        for i in range(1, 7):
            subject_name =request.form.get(f"subject_{i}")
            marks = request.form.get(f"marks_{i}")
            if subject_name and marks:
                cursor.execute(
                    "INSERT INTO subjects (student_id, subject_name, marks) values (?,?,?)", (student_id, subject_name, float(marks))
                )
        conn.commit()
        conn.close()
        return redirect(url_for("home"))
    return render_template("add.html")
@app.route("/student/<int:id>")
def student_detail(id):
    conn = get_db()
    cursor = conn.cursor()
    
   
    cursor.execute("SELECT * FROM student WHERE id = ?", (id,))
    student = cursor.fetchone()
    
    
    cursor.execute("SELECT * FROM subjects WHERE student_id = ?", (id,))
    subjects = cursor.fetchall()
    conn.close()
    
    
    subject_list = []
    for s in subjects:
        gpa, grade = calculate_gpa(s["marks"])
        subject_list.append({
            "name": s["subject_name"],
            "marks": s["marks"],
            "grade": grade,
            "gpa": gpa
        })
    
    if subject_list:
        avg_marks = sum(s["marks"] for s in subject_list) / len(subject_list)
        overall_gpa, overall_grade = calculate_gpa(avg_marks)
        percentage = round(avg_marks, 2)
    else:
        percentage = overall_gpa = 0
        overall_grade = "N/A"
    
    return render_template("student.html",
                         student=student,
                         subjects=subject_list,
                         percentage=percentage,
                         overall_gpa=overall_gpa,
                         overall_grade=overall_grade)
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subjects WHERE student_id = ?", (id,))
    cursor.execute("DELETE FROM student WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))
@app.route("/edit/<int:id>")
def edit(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE id = ?", (id,))
    student = cursor.fetchone()
    cursor.execute("SELECT * FROM subjects WHERE student_id = ?", (id,))
    subjects = cursor.fetchall()
    conn.close()
    return render_template("edit.html", student=student, subjects=subjects)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    conn = get_db()
    cursor = conn.cursor()
    for i in range(1, 7):
        subject_id = request.form.get(f"subject_id_{i}")
        marks = request.form.get(f"marks_{i}")
        if subject_id and marks:
            cursor.execute(
                "UPDATE subjects SET marks = ? WHERE id = ?",
                (float(marks), int(subject_id))
            )
    conn.commit()
    conn.close()
    return redirect(url_for("student_detail", id=id))
@app.route("/search")
def search():
    query = request.args.get("q")  # get search query from URL
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE name LIKE ?", (f"%{query}%",))
    students = cursor.fetchall()
    conn.close()
    return render_template("home.html", students=students, query=query)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
