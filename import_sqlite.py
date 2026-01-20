import sqlite3

DB_FILE = "sds.db"
SQL_FILE = "sds_local.sql"   # 你项目里已经有这个文件

with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql = f.read()

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()
cur.executescript(sql)
conn.commit()

print("✅ Imported SQL into", DB_FILE)
print("students count =", cur.execute("SELECT COUNT(*) FROM students").fetchone()[0])

conn.close()
