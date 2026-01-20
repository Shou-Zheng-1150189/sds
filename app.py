from flask import Flask, render_template, request, redirect, url_for
import os
import re
import sqlite3
from datetime import date

import db
import connect

app = Flask(__name__)
app.secret_key = "sds_secret_2025"

# 用 SQLite 初始化（connect.db 是数据库文件路径）
db.init_db(app, connect.db)

# -----------------------
# Helpers
# -----------------------
def pick_template(primary: str, fallback: str) -> str:
    """优先用 primary 模板；如果不存在就用 fallback（避免模板文件名不一致导致 500）"""
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    if os.path.exists(os.path.join(templates_dir, primary)):
        return primary
    return fallback


def _is_valid_email(email: str) -> bool:
    # 轻量 email 检查（够用）
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


# -----------------------
# Routes
# -----------------------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/teachers")
def teachers():
    cur = db.get_cursor()
    try:
        cur.execute("""
            SELECT teacher_id, first_name, last_name
            FROM teachers
            ORDER BY last_name, first_name;
        """)
        teacher_rows = cur.fetchall()
    finally:
        cur.close()

    template = pick_template("teachers.html", "teacher_list.html")
    return render_template(template, teachers=teacher_rows)


@app.route("/students")
def students():
    q = request.args.get("q", "").strip()

    cur = db.get_cursor()
    try:
        if q:
            like = f"%{q}%"
            cur.execute("""
                SELECT student_id, first_name, last_name, email, phone, date_of_birth, enrollment_date, is_active
                FROM students
                WHERE first_name LIKE ? OR last_name LIKE ?
                ORDER BY last_name, first_name;
            """, (like, like))
        else:
            cur.execute("""
                SELECT student_id, first_name, last_name, email, phone, date_of_birth, enrollment_date, is_active
                FROM students
                ORDER BY last_name, first_name;
            """)
        student_rows = cur.fetchall()
    finally:
        cur.close()

    return render_template("student_list.html", students=student_rows, q=q)


@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    message = None
    errors = {}
    today_iso = date.today().isoformat()

    # GET：显示空表单
    if request.method == "GET":
        return render_template(
            "add_student.html",
            message=None,
            errors={},
            form={
                "first_name": "",
                "last_name": "",
                "email": "",
                "phone": "",
                "date_of_birth": "",
                "enrollment_date": today_iso,
            }
        )

    # POST：处理提交
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()

    date_of_birth = request.form.get("date_of_birth", "").strip()
    enrollment_date = request.form.get("enrollment_date", "").strip() or today_iso

    # 你模板里是 status Active/Inactive，这里统一转成 is_active 1/0
    status = request.form.get("status", "Active").strip()
    is_active = 1 if status.lower() == "active" else 0

    # Validation
    if not first_name:
        errors["first_name"] = "First name is required."
    if not last_name:
        errors["last_name"] = "Last name is required."

    if email and not _is_valid_email(email):
        errors["email"] = "Email format looks invalid."

    if not date_of_birth:
        errors["date_of_birth"] = "Date of birth is required."
    else:
        try:
            dob = date.fromisoformat(date_of_birth)
            if dob > date.today():
                errors["date_of_birth"] = "Date of birth cannot be in the future."
        except ValueError:
            errors["date_of_birth"] = "Invalid date format."

    try:
        ed = date.fromisoformat(enrollment_date)
        if ed > date.today():
            errors["enrollment_date"] = "Date joined cannot be in the future."
    except ValueError:
        errors["enrollment_date"] = "Invalid date format."

    # Insert
    if not errors:
        cur = db.get_cursor()
        try:
            cur.execute("""
                INSERT INTO students (first_name, last_name, email, phone, date_of_birth, enrollment_date, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (first_name, last_name, email or None, phone or None, date_of_birth, enrollment_date, is_active))
            cur.connection.commit()
            new_id = cur.lastrowid
        finally:
            cur.close()

        message = f"✅ Student added successfully (ID {new_id})."

        # 成功后清空表单
        return render_template(
            "add_student.html",
            message=message,
            errors={},
            form={
                "first_name": "",
                "last_name": "",
                "email": "",
                "phone": "",
                "date_of_birth": "",
                "enrollment_date": today_iso,
            }
        )

    # 有错误：回填表单
    form = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "date_of_birth": date_of_birth,
        "enrollment_date": enrollment_date,
        "status": status,
    }
    return render_template("add_student.html", message=None, errors=errors, form=form)


@app.route("/classes")
def classes():
    cur = db.get_cursor()
    try:
        cur.execute("""
            SELECT
                c.class_id,
                c.class_name,
                c.schedule_day,
                c.schedule_time,
                d.dancetype_name,
                g.grade_name,
                g.grade_level,
                t.first_name AS teacher_first_name,
                t.last_name  AS teacher_last_name
            FROM classes c
            JOIN dancetype d ON c.dancetype_id = d.dancetype_id
            JOIN grades g ON c.grade_id = g.grade_id
            JOIN teachers t ON c.teacher_id = t.teacher_id
            ORDER BY d.dancetype_name, g.grade_level, c.class_name;
        """)
        class_rows = cur.fetchall()

        cur.execute("""
            SELECT
                sc.class_id,
                s.student_id,
                s.first_name,
                s.last_name
            FROM studentclasses sc
            JOIN students s ON sc.student_id = s.student_id
            ORDER BY sc.class_id, s.last_name, s.first_name;
        """)
        enrol_rows = cur.fetchall()
    finally:
        cur.close()

    students_by_class = {}
    for r in enrol_rows:
        cid = r["class_id"]
        students_by_class.setdefault(cid, []).append(r)

    return render_template("classes.html", classes=class_rows, students_by_class=students_by_class)


@app.route("/students/<int:student_id>")
def student_summary(student_id):
    cur = db.get_cursor()
    try:
        cur.execute("""
            SELECT student_id, first_name, last_name
            FROM students
            WHERE student_id = ?;
        """, (student_id,))
        student = cur.fetchone()

        cur.execute("""
            SELECT
                c.class_id,
                c.class_name,
                d.dancetype_name,
                g.grade_name,
                g.grade_level,
                c.schedule_day,
                c.schedule_time,
                t.first_name AS teacher_first_name,
                t.last_name  AS teacher_last_name
            FROM studentclasses sc
            JOIN classes c ON sc.class_id = c.class_id
            JOIN dancetype d ON c.dancetype_id = d.dancetype_id
            JOIN grades g ON c.grade_id = g.grade_id
            JOIN teachers t ON c.teacher_id = t.teacher_id
            WHERE sc.student_id = ?
            ORDER BY d.dancetype_name, g.grade_level, c.class_name;
        """, (student_id,))
        classes_rows = cur.fetchall()
    finally:
        cur.close()

    return render_template("student_summary.html", student=student, classes=classes_rows)


@app.route("/students/<int:student_id>/enrol", methods=["GET", "POST"])
def enrol_student(student_id):
    cur = db.get_cursor()
    try:
        cur.execute("""
            SELECT student_id, first_name, last_name
            FROM students
            WHERE student_id = ?;
        """, (student_id,))
        student = cur.fetchone()
        if not student:
            return render_template("enrol.html", student=None, eligible_classes=[], message="Student not found.")

        cur.execute("""
            SELECT MAX(g.grade_level) AS current_level
            FROM studentgrades sg
            JOIN grades g ON sg.grade_id = g.grade_id
            WHERE sg.student_id = ?;
        """, (student_id,))
        row = cur.fetchone()
        current_level = row["current_level"] if row and row["current_level"] is not None else None
        max_level_allowed = None if current_level is None else current_level + 1

        if max_level_allowed is None:
            cur.execute("""
                SELECT
                    c.class_id, c.class_name,
                    d.dancetype_name, g.grade_name, g.grade_level,
                    t.first_name AS teacher_first_name, t.last_name AS teacher_last_name,
                    c.schedule_day, c.schedule_time
                FROM classes c
                JOIN dancetype d ON c.dancetype_id = d.dancetype_id
                JOIN grades g ON c.grade_id = g.grade_id
                JOIN teachers t ON c.teacher_id = t.teacher_id
                WHERE c.class_id NOT IN (
                    SELECT class_id FROM studentclasses WHERE student_id = ?
                )
                ORDER BY d.dancetype_name, g.grade_level, c.class_name;
            """, (student_id,))
        else:
            cur.execute("""
                SELECT
                    c.class_id, c.class_name,
                    d.dancetype_name, g.grade_name, g.grade_level,
                    t.first_name AS teacher_first_name, t.last_name AS teacher_last_name,
                    c.schedule_day, c.schedule_time
                FROM classes c
                JOIN dancetype d ON c.dancetype_id = d.dancetype_id
                JOIN grades g ON c.grade_id = g.grade_id
                JOIN teachers t ON c.teacher_id = t.teacher_id
                WHERE g.grade_level <= ?
                  AND c.class_id NOT IN (
                      SELECT class_id FROM studentclasses WHERE student_id = ?
                  )
                ORDER BY d.dancetype_name, g.grade_level, c.class_name;
            """, (max_level_allowed, student_id))

        eligible_classes = cur.fetchall()
        message = None

        if request.method == "POST":
            class_id = request.form.get("class_id", "").strip()

            if not class_id.isdigit():
                message = "Please select a class."
            else:
                class_id_int = int(class_id)
                eligible_ids = {c["class_id"] for c in eligible_classes}

                if class_id_int not in eligible_ids:
                    message = "You cannot enrol in this class (not eligible or already enrolled)."
                else:
                    cur.execute("""
                        INSERT INTO studentclasses (student_id, class_id)
                        VALUES (?, ?);
                    """, (student_id, class_id_int))
                    cur.connection.commit()

                    return render_template(
                        "enrol.html",
                        student=student,
                        eligible_classes=[],
                        message="✅ Enrolment saved successfully!"
                    )

    finally:
        cur.close()

    return render_template("enrol.html", student=student, eligible_classes=eligible_classes, message=message)


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    message = None
    errors = {}

    cur = db.get_cursor()
    try:
        cur.execute("""
            SELECT student_id, first_name, last_name, email, phone, date_of_birth, enrollment_date, is_active
            FROM students
            WHERE student_id = ?;
        """, (student_id,))
        student = cur.fetchone()
        if not student:
            return render_template(
                "edit_student.html",
                student=None, grades=[], current_grade_id=None,
                errors={}, message="Student not found."
            )

        cur.execute("""
            SELECT grade_id, grade_name, grade_level
            FROM grades
            ORDER BY grade_level;
        """)
        grades = cur.fetchall()

        cur.execute("""
            SELECT sg.grade_id
            FROM studentgrades sg
            JOIN grades g ON sg.grade_id = g.grade_id
            WHERE sg.student_id = ?
            ORDER BY g.grade_level DESC
            LIMIT 1;
        """, (student_id,))
        row = cur.fetchone()
        current_grade_id = row["grade_id"] if row else None

        if request.method == "POST":
            first_name = request.form.get("first_name", "").strip()
            last_name = request.form.get("last_name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            date_of_birth = request.form.get("date_of_birth", "").strip()
            is_active = 1 if request.form.get("is_active") == "1" else 0
            new_grade_id = request.form.get("grade_id", "").strip()

            if not first_name:
                errors["first_name"] = "First name is required."
            if not last_name:
                errors["last_name"] = "Last name is required."
            if email and not _is_valid_email(email):
                errors["email"] = "Email format looks invalid."

            if not date_of_birth:
                errors["date_of_birth"] = "Date of birth is required."
            else:
                try:
                    dob = date.fromisoformat(date_of_birth)
                    if dob > date.today():
                        errors["date_of_birth"] = "Date of birth cannot be in the future."
                except ValueError:
                    errors["date_of_birth"] = "Invalid date format."

            if not new_grade_id.isdigit():
                errors["grade_id"] = "Please choose a grade."

            if not errors:
                cur.execute("""
                    UPDATE students
                    SET first_name = ?, last_name = ?, email = ?, phone = ?, date_of_birth = ?, is_active = ?
                    WHERE student_id = ?;
                """, (first_name, last_name, email or None, phone or None, date_of_birth, is_active, student_id))

                new_grade_id_int = int(new_grade_id)
                cur.execute("DELETE FROM studentgrades WHERE student_id = ?;", (student_id,))
                cur.execute("""
                    INSERT INTO studentgrades (student_id, grade_id)
                    VALUES (?, ?);
                """, (student_id, new_grade_id_int))

                cur.connection.commit()
                message = "✅ Student updated successfully."
                current_grade_id = new_grade_id_int

                cur.execute("""
                    SELECT student_id, first_name, last_name, email, phone, date_of_birth, enrollment_date, is_active
                    FROM students
                    WHERE student_id = ?;
                """, (student_id,))
                student = cur.fetchone()

        return render_template(
            "edit_student.html",
            student=student,
            grades=grades,
            current_grade_id=current_grade_id,
            errors=errors,
            message=message
        )
    finally:
        cur.close()


@app.route("/report/teachers")
def teacher_report():
    conn = sqlite3.connect(connect.db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute("""
        SELECT
            t.teacher_id,
            t.first_name,
            t.last_name,
            COUNT(c.class_id) AS class_count
        FROM teachers t
        LEFT JOIN classes c ON c.teacher_id = t.teacher_id
        GROUP BY t.teacher_id, t.first_name, t.last_name
        ORDER BY t.last_name, t.first_name;
    """).fetchall()

    conn.close()
    return render_template("teacher_report.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
