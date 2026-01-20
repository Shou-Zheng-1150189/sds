import sqlite3
import os

# 明确打印当前工作目录（用于调试）
print("Current working directory:", os.getcwd())

db_path = os.path.join(os.getcwd(), "sds.db")
print("Database path:", db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

print("\nTables in database:")
if tables:
    for t in tables:
        print("-", t[0])
else:
    print("⚠️ No tables found!")

conn.close()
