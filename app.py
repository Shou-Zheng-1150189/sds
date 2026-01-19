from flask import Flask, render_template

import db
import connect

app = Flask(__name__)

# 用 SQLite 初始化数据库
db.init_db(app, connect.db)
