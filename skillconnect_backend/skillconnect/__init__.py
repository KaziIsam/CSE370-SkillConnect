# This file patches Django to use pymysql instead of mysqlclient.
# pymysql works with MySQL 8.0.44 without any password/auth issues.
import pymysql
pymysql.install_as_MySQLdb()
