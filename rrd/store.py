#-*- coding:utf-8 -*-
import MySQLdb
from rrd import config

def connect_db(host, port, user, password, db):
    try:
        conn = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=db,
            use_unicode=True,
            charset="utf8")
        conn.autocommit(True)
        return conn
    except Exception, e:
        print 'level=fatal msg="connect db fail:%s"' % e
        return None

class DB(object):

    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self._conn = connect_db(host, port, user, password, db)

    def connect(self):
        self._conn = connect_db(self.host, self.port, self.user, self.password, self.db)
        return self._conn

    def execute(self, *a, **kw):
        cursor = kw.pop('cursor', None)
        try:
            cursor = cursor or self._conn.cursor()
            cursor.execute(*a, **kw)
        except (AttributeError, MySQLdb.OperationalError):
            self._conn and self._conn.close()
            self.connect()
            cursor = self._conn.cursor()
            cursor.execute(*a, **kw)
        return cursor

    def commit(self):
        if self._conn:
            try:
                self._conn.commit()
            except MySQLdb.OperationalError:
                self._conn and self._conn.close()
                self.connect()
                self._conn and self._conn.commit()

    def rollback(self):
        if self._conn:
            try:
                self._conn.rollback()
            except MySQLdb.OperationalError:
                self._conn and self._conn.close()
                self.connect()
                self._conn and self._conn.rollback()

dashboard_db_conn = DB(
        config.DASHBOARD_DB_HOST,
        config.DASHBOARD_DB_PORT,
        config.DASHBOARD_DB_USER,
        config.DASHBOARD_DB_PASS,
        config.DASHBOARD_DB_NAME)

graph_db_conn = DB(
        config.GRAPH_DB_HOST,
        config.GRAPH_DB_PORT,
        config.GRAPH_DB_USER,
        config.GRAPH_DB_PASS,
        config.GRAPH_DB_NAME)

portal_db_conn = DB(
        config.PORTAL_DB_HOST,
        config.PORTAL_DB_PORT,
        config.PORTAL_DB_USER,
        config.PORTAL_DB_PASS,
        config.PORTAL_DB_NAME)
