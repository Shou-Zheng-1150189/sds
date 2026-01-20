import sqlite3
from datetime import date

DB_FILE = "sds.db"

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# 1) 插入 3 个学生（如果表里还没有任何学生）
count = cur.execute("SELECT COUNT(*) FROM students").fetchone()[0]
print("Before insert, students count =", count)

if count == 0:
    today = date.today().isoformat()

    # students 表字段：student_id 自动，email 可为空
    students = [
        ("Aroha", "Ngata", None, "021111111", "2012-05-10", today, 1),
        ("Mei", "Chen", "mei.chen@example.com", "021222222", "2011-09-21", today, 1),
        ("Tom", "Wilson", "tom.w@example.com", "021333333", "2010-02-03", today, 1),
    ]

    cur.executemany("""
        INSERT INTO students (first_name, last_name, email, phone, date_of_birth, enrollment_date, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, students)

    print("✅ Inserted 3 students.")
else:
    print("Students already exist, skip inserting students.")

# 2) 给这些学生报名一些课（如果 classes 表有课）
cur.execute("SELECT class_id FROM classes ORDER BY class_id LIMIT 3;")
class_ids = [r[0] for r in cur.fetchall()]

if class_ids:
    # 取刚插入/已存在的前3个学生
    cur.execute("SELECT student_id FROM students ORDER BY student_id LIMIT 3;")
    student_ids = [r[0] for r in cur.fetchall()]

    # 清掉这3个学生在这几门课的重复报名（避免重复）
    for sid in student_ids:
        for cid in class_ids:
            cur.execute("DELETE FROM studentclasses WHERE student_id=? AND class_id=?;", (sid, cid))

    # 报名：每个学生报1-2门课
    enrolments = [
        (student_ids[0], class_ids[0]),
        (student_ids[0], class_ids[1]),
        (student_ids[1], class_ids[1]),
        (student_ids[2], class_ids[2]),
    ]
    cur.executemany("INSERT INTO studentclasses (student_id, class_id) VALUES (?, ?);", enrolments)
    print("✅ Added some enrolments in studentclasses.")
else:
    print("⚠️ No classes found in classes table. Skipped enrolments.")

conn.commit()

# 最后再显示数量
count_after = cur.execute("SELECT COUNT(*) FROM students").fetchone()[0]
print("After insert, students count =", count_after)

conn.close()
print("Done.")
