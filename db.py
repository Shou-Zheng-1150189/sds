import sqlite3
from flask import current_app, g


def init_db(app, db_path: str):
    """把数据库路径放进 Flask config，并注册 teardown 自动关闭连接"""
    app.config["DATABASE"] = db_path
    app.teardown_appcontext(close_db)


def get_db():
    """每个 request 复用同一个连接（存在 g 里）"""
    if "db_conn" not in g:
        conn = sqlite3.connect(current_app.config["DATABASE"])
        conn.row_factory = sqlite3.Row  # fetch 时可以用 row["col"] 或 row.col
        g.db_conn = conn
    return g.db_conn


def get_cursor():
    return get_db().cursor()


def close_db(e=None):
    """每个 request 结束自动关闭连接"""
    conn = g.pop("db_conn", None)
    if conn is not None:
        conn.close()
