import os

# SQLite 数据库文件路径（与你的 app.py 同目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(BASE_DIR, "sds.db")
