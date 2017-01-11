# -*- coding:utf-8 -*-

from __future__ import absolute_import

from werkzeug.utils import import_string
from flask import Flask
from flask import request
from flask import redirect
import MySQLdb
import time
from contextlib import closing
import json
from . import config
import logging
from raven.contrib.flask import Sentry


logger = logging.getLogger(__name__)
if config.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
sentry = Sentry(register_signal=False)


def queryDB(sig):
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
    rows = None
    table = config.UIC_DB_TABLE_SESSION
    fields = 'expired'
    where = '`sig`="' + sig + '"'
    sql = 'SELECT ' + fields + ' FROM `' + table + '`' + ' WHERE ' + where
    mydb = MySQLdb.connect(
        host=config.UIC_DB_HOST,
        port=int(config.UIC_DB_PORT),
        user=config.UIC_DB_USER,
        passwd=config.UIC_DB_PASS,
        db=config.UIC_DB_NAME,
        charset='utf8'
    )

    with closing(mydb.cursor()) as cursor:
        args = None
        cursor.execute(sql, args)
        rows = cursor.fetchall()
        mydb.commit()

    mydb.close()
    return rows


blueprints = [
    'rrd.view.index:bp',
    'rrd.view.api:bp',
    'rrd.view.chart:bp',
    'rrd.view.screen:bp',
]


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    sentry.init_app(app)

    API_PATHS = ['/api', '/chart']

    @app.errorhandler(Exception)
    def all_exception_handler(error):
        logger.warning('msg="exception: %r"' % error)
        resp = {
            "status": "failed",
            "msg": u'dashboard got some problem now, please contact your system admin.'
        }
        return json.dumps(resp), 500

    # from .view import api, chart, screen, index
    for bp in map(import_string, blueprints):
        app.register_blueprint(bp)

    @app.before_request
    def before_request():
        path = request.path
        for api_path in API_PATHS:
            if path.startswith(api_path):
                return

        sig = request.cookies.get('sig')
        url = config.JSONCFG['redirectUrl']
        if not sig:
            logger.info(
                'sig is missing in request.cookies from %s' %
                request.remote_addr)
            return redirect(url, code=302)

        rows = queryDB(sig)
        if rows is None or len(rows) == 0:
            logger.info('sig: %s not found' % sig)
            return redirect(url, code=302)

        row = rows[0]
        expiredTime = row[0]
        now = int(time.time())
        expired = now > expiredTime
        if expired:
            logger.warning('sig: %s is expired' % sig)
            return redirect(url, code=302)

        logger.debug('signed OK')

    return app
