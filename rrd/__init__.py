#-*- coding:utf-8 -*-
import os
from flask import Flask
from flask import request
from flask import redirect
import MySQLdb
import datetime
import time
from contextlib import closing
import json

"""
* @def name:        queryDB(config, sig)
* @description:     This function returns query result of given SQL command.
* @related issues:  OWL-265, OWL-117
* @param:           list config
* @param:           string sig
* @return:          list rows
* @author:          Don Hsieh
* @since:           10/13/2015
* @last modified:   01/08/2016
* @called by:       def index()
*                    in rrd/view/index.py
"""
def queryDB(sig):
    rows = None
    table = config.JSONCFG['database']['table']
    fields = 'expired'
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

API_PATHS = ['/api', '/chart']

@app.errorhandler(Exception)
def all_exception_handler(error):
    print 'msg="exception: %s"' % error
    resp = {
             "status": "failed",
             "msg": u'dashboard got some problem now, please contact your system admin.'
           }
    return json.dumps(resp), 500

from view import api, chart, screen, index
@app.before_request
def before_request():
    path = request.path
    for api_path in API_PATHS:
        if path.startswith(api_path):
            return

    sig = request.cookies.get('sig')
    url = config.JSONCFG['redirectUrl']
    if not sig:
        return redirect(url, code=302)

    rows = queryDB(sig)
    if rows is None or len(rows) == 0:
        return redirect(url, code=302)

    row = rows[0]
    expiredTime = row[0]
    now = int(time.time())
    expired = now > expiredTime
    if expired:
        return redirect(url, code=302)
