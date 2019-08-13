import pymysql.cursors
import os

# Function return a connection.
def getConnection():
     # You can change the connection arguments.
     connection = pymysql.connect(user='temp_vscan',
                                 password='temp_vscan',
                                host="192.168.202.24",
                                db="TEMP_VSCAN", charset="utf8mb4",
                                cursorclass=pymysql.cursors.DictCursor)
     return connection
