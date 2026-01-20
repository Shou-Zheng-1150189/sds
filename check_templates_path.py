import os
from app import app

print("=== Flask template search info ===")
print("app.root_path =", app.root_path)
print("app.template_folder =", app.template_folder)
print("jinja_loader.searchpath =", app.jinja_loader.searchpath)

# 看看 add_student.html 是否在 Flask 认为的 templates 目录里
for p in app.jinja_loader.searchpath:
    target = os.path.join(p, "add_student.html")
    print("check:", target, "exists =", os.path.exists(target))

