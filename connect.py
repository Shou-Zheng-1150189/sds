import os

# ===== Local (Windows / 本地) =====
LOCAL_DBUSER = "root"
LOCAL_DBPASS = "sds1234sds1234"
LOCAL_DBHOST = "127.0.0.1"
LOCAL_DBPORT = 3306
LOCAL_DBNAME = "sds"

# ===== PythonAnywhere =====
PA_DBUSER = "ShouZheng1150189"
PA_DBPASS = "Popcorn0818!Password0818!"
PA_DBHOST = "ShouZheng1150189.mysql.pythonanywhere-services.com"
PA_DBPORT = 3306
PA_DBNAME = "ShouZheng1150189$default"

# ===== 自动判断运行环境 =====
if os.environ.get("PYTHONANYWHERE_DOMAIN"):
    dbuser = PA_DBUSER
    dbpass = PA_DBPASS
    dbhost = PA_DBHOST
    dbport = PA_DBPORT
    dbname = PA_DBNAME
else:
    dbuser = LOCAL_DBUSER
    dbpass = LOCAL_DBPASS
    dbhost = LOCAL_DBHOST
    dbport = LOCAL_DBPORT
    dbname = LOCAL_DBNAME
