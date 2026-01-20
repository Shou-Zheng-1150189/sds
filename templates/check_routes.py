import re

with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

routes = re.findall(r'@app\.route\("/students"', text)

print("Number of /students routes found:", len(routes))
print("Routes detail:")
for r in routes:
    print(r)
