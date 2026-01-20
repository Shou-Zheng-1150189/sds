import sqlite3

DB_FILE = "sds.db"
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

def count(table):
    return cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

print("Before:")
for t in ["teachers", "grades", "dancetype", "classes"]:
    print(t, "=", count(t))

# 1) teachers
if count("teachers") == 0:
    cur.executemany("""
        INSERT INTO teachers (first_name, last_name, email, phone, is_active)
        VALUES (?, ?, ?, ?, ?);
    """, [
        ("Anna", "Brown", "anna.brown@example.com", "021000001", 1),
        ("James", "Lee", "james.lee@example.com", "021000002", 1),
    ])
    print("✅ Inserted teachers")

# 2) grades
if count("grades") == 0:
    cur.executemany("""
        INSERT INTO grades (grade_name, grade_level)
        VALUES (?, ?);
    """, [
        ("Beginner", 1),
        ("Intermediate", 2),
        ("Advanced", 3),
    ])
    print("✅ Inserted grades")

# 3) dancetype
if count("dancetype") == 0:
    cur.executemany("""
        INSERT INTO dancetype (dancetype_name)
        VALUES (?);
    """, [
        ("Ballet",),
        ("Jazz",),
    ])
    print("✅ Inserted dancetype")

# 4) classes (need teacher_id, grade_id, dancetype_id)
if count("classes") == 0:
    teacher_ids = [r[0] for r in cur.execute("SELECT teacher_id FROM teachers ORDER BY teacher_id").fetchall()]
    grade_ids = [r[0] for r in cur.execute("SELECT grade_id, grade_level FROM grades ORDER BY grade_level").fetchall()]
    dancetype_ids = [r[0] for r in cur.execute("SELECT dancetype_id FROM dancetype ORDER BY dancetype_id").fetchall()]

    # 简单创建 3 个课程
    cur.executemany("""
        INSERT INTO classes (class_name, dancetype_id, grade_id, teacher_id, schedule_day, schedule_time)
        VALUES (?, ?, ?, ?, ?, ?);
    """, [
        ("Ballet Beginners", dancetype_ids[0], grade_ids[0], teacher_ids[0], "Mon", "16:00"),
        ("Ballet Intermediate", dancetype_ids[0], grade_ids[1], teacher_ids[0], "Wed", "17:00"),
        ("Jazz Beginners", dancetype_ids[1], grade_ids[0], teacher_ids[1], "Fri", "16:30"),
    ])
    print("✅ Inserted classes")

conn.commit()

print("\nAfter:")
for t in ["teachers", "grades", "dancetype", "classes"]:
    print(t, "=", count(t))

conn.close()
print("Done.")
