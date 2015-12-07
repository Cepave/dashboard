#-*- coding:utf-8 -*-
import os
from flask import Flask
from flask import request
from flask import redirect
import MySQLdb
import datetime
import time
from contextlib import closing

"""
* @def name:        queryDB(config, sig)
* @description:     This function returns query result of given SQL command.
* @related issues:  OWL-117
* @param:           list config
* @param:           string sig
* @return:          list rows
* @author:          Don Hsieh
* @since:           10/13/2015
* @last modified:   10/14/2015
* @called by:       def index()
*                    in rrd/view/index.py
"""
def queryDB(sig):
    rows = None
    table = config.JSONCFG['database']['table']
    fields = 'id, expired'
    where = '`sig`="' + sig + '"'
    sql = 'SELECT ' + fields + ' FROM `' + table + '`' + ' WHERE ' + where
    mydb = MySQLdb.connect(
        host=config.JSONCFG['database']['host'],
        port=int(config.JSONCFG['database']['port']),
        user=config.JSONCFG['database']['account'],
        passwd=config.JSONCFG['database']['password'],
        db=config.JSONCFG['database']['db'],
        charset='utf8'
    )

    with closing(mydb.cursor()) as cursor:
        args = None
        cursor.execute(sql, args)
        rows = cursor.fetchall()
        mydb.commit()

    mydb.close()
    return rows

#-- create app --
app = Flask(__name__)
app.config.from_object("rrd.config")

@app.errorhandler(Exception)
def all_exception_handler(error):
    print "exception: %s" %error
    return u'dashboard 暂时无法访问，请联系管理员', 500

from view import api, chart, screen, index
@app.before_request
def before_request():
    f = open('dashboard.log', 'a')
    current_time = datetime.datetime.now()
    f.write('\n' + 'current_time = ' + str(current_time) + '\n')
    f.write('request.path = ' + request.path + '\n')
    if '/api/' in request.path:
        f.close()
    else:
        sig = request.cookies.get('sig')
        f.write("sig = %s \n" %sig)
        url = config.JSONCFG['redirectUrl']
        if not sig:
            f.close()
            return redirect(url, code=302)
        else:
            rows = queryDB(sig)
            if rows is None or len(rows) == 0:
                f.close()
                return redirect(url, code=302)

            f.write('rows = ' + str(rows) + '\n')
            row = rows[0]
            id = row[0]
            expiredTime = row[1]
            current_time = datetime.datetime.now()

            now = int(time.time())
            f.write('now = ' + str(now) + '\n')
            f.write('expired time = ' + str(expiredTime) + '\n')
            expired = now > expiredTime
            f.write('expired = ' + str(expired) + '\n')
            f.close()
            if expired:
                return redirect(url, code=302)