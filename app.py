from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import db
import connect

app = Flask(__name__)
app.secret_key = "sds_secret_2025"

# -------------------------------------------------
# Database initialisation
# -------------------------------------------------
db.init_db(
    app,
    connect.dbuser,
    connect.dbpass,
    connect.dbhost,
    connect.dbname,
    connect.dbport
)

# -------------------------------------------------
# Home page
# -------------------------------------------------
@app.route("/")
def home():
    """
    Home page:
    show a small list of recent students
    """
    cursor = db.get_cursor()

    cursor.execute("""
        SELECT student_id, first_name, last_name
        FROM students
        ORDER BY enrollment_date DESC
        LIMIT 10
    """)

    students = cursor.fetchall()
    cursor.close()

    return render_template("home.html", students=students)


# -------------------------------------------------
# Teachers
# -------------------------------------------------
@app.route("/teachers")
def teacher_list():
    """
    List all teachers
    """
    cursor = db.get_cursor()

    cursor.execute("""
        SELECT teacher_id, first_name, last_name, email, phone
        FROM teachers
        ORDER BY last_name, first_name
    """)

    teachers = cursor.fetchall()
    cursor.close()

    return render_template("teacher_list.html", teachers=teachers)


# -------------------------------------------------
# Students
# -------------------------------------------------
@app.route("/students")
def student_list():
    """
    List all students
    """
    cursor = db.get_cursor()

    cursor.execute("""
        SELECT
            student_id,
            first_name,
            last_name,
            email,
            phone,
            date_of_birth,
            enrollment_date,
            is_active
        FROM students
        ORDER BY last_name, first_name
    """)

    students = cursor.fetchall()
    cursor.close()

    return render_template("student_list.html", students=students)


# -------------------------------------------------
# Run guard (optional, but good practice)
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
