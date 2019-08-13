import sys
import pandas as pd
import flask
import jinja2
import jinja2.ext
from jinja2 import escape
from flask import Flask, render_template, request, flash, request, redirect, url_for, jsonify
import pymysql.cursors
import pymysql
import os
import connect_db

sys.setrecursionlimit(5000)
connection = connect_db.getConnection()

try:
    app = flask.Flask(__name__, template_folder=os.path.abspath(os.getcwd() + "/gui/"), static_folder=os.path.abspath(os.getcwd() + "/gui/static"))
    # app.secret_key = 'V2 Solutions'
except Exception as e:
    print("3. Exception Occurred: {}".format(e))
    app = flask.Flask(__name__)
    exit()

@app.route("/result", methods=["GET", "POST"])
def result():
    def getConnection():
        db_cred = open("database.txt", "r")

        host = db_cred.readline()
        user = db_cred.readline()
        pwd = db_cred.readline()
        port = db_cred.readline()
        host = host.strip(' Host:\n')
        user = user.strip('User:\n')
        user = user.strip(' ')
        pwd = pwd.strip('Password:\n')
        pwd = pwd.strip(' ')
        port = port.strip('Port: ')
        port = port.strip(' ')
        port = int(port)
        dbname = "TEMP_VSCAN"
        crsrclass = pymysql.cursors.DictCursor

        connection = pymysql.connections.Connection
        try:
            connection = pymysql.connect(user=user, password=pwd, host=host, port=port, db=dbname, charset="utf8mb4",
                                         cursorclass=crsrclass)

        except Exception as e:
            print("14. Exception Occurred: {}".format(e))
        finally:
            return connection

    def runstats1(col, jid):
        table = pd.DataFrame()
        table_name = 'Runstats_Summary'
        # print(col,jid)
        query0 = 'select * from ' + table_name + ';'
        query1 = 'select * from ' + table_name + ' where Job_id="' + jid + '";'
        query2 = 'select * from ' + table_name + ' where date="' + jid + '";'

        if col == 1:
            table = Query1(query0)
            # print(table)
        elif col == 2:
            table = Query1(query1)
            # print(table)
        elif col == 3:
            table = Query1(query2)

        return table

    def Query1(query):
        connection = getConnection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                df = pd.read_sql(query, connection)
                # print(df.columns)
            connection.close()
            return df
        except Exception as e:
            print("15. Exception Occurred: {}".format(e))
            return pd.DataFrame()

    df4 = pd.DataFrame()
    jid = ''
    if flask.request.method == 'POST':
        jid = flask.request.form.get('tbox')
        filterby = flask.request.form.get('filterby')
        if filterby == 'jobid':
            df4 = runstats1(2, jid)
        elif filterby == 'date':
            df4 = runstats1(3, jid)

    df3 = runstats1(1, '')
    df3 = df3.sort_values(['Job_id'],axis = 0,ascending=False)
    return flask.render_template('template_result.html', table1=[df3.to_html(classes='data', header=True,
                                                                                  index=False)],
                                 table2=[df4.to_html(classes='data', header=True, index=False)], jid=jid)

if __name__ == '__main__':
    app.run(port=8000, host='192.168.202.80', debug=True)
