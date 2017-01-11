# -*-coding:utf8-*-

from __future__ import absolute_import

from decouple import config


# -- dashboard db config --
DASHBOARD_DB_HOST = config('FALCON_DASHBOARD_DB_HOST', default="127.0.0.1")
DASHBOARD_DB_PORT = config('FALCON_DASHBOARD_DB_PORT', default=3306, cast=int)
DASHBOARD_DB_USER = config('FALCON_DASHBOARD_DB_USER', default="root")
DASHBOARD_DB_PASS = config('FALCON_DASHBOARD_DB_PASS', default="password")
DASHBOARD_DB_NAME = config('FALCON_DASHBOARD_DB_NAME', default="dashboard")

# -- graph db config --
GRAPH_DB_HOST = config('FALCON_GRAPH_DB_HOST', default="127.0.0.1")
GRAPH_DB_PORT = config('FALCON_GRAPH_DB_PORT', default=3306, cast=int)
GRAPH_DB_USER = config('FALCON_GRAPH_DB_USER', default="root")
GRAPH_DB_PASS = config('FALCON_GRAPH_DB_PASS', default="password")
GRAPH_DB_NAME = config('FALCON_GRAPH_DB_NAME', default="graph")

# -- portal db config --
PORTAL_DB_HOST = config('FALCON_PORTAL_DB_HOST', default="127.0.0.1")
PORTAL_DB_PORT = config('FALCON_PORTAL_DB_PORT', default=3306, cast=int)
PORTAL_DB_USER = config('FALCON_PORTAL_DB_USER', default="root")
PORTAL_DB_PASS = config('FALCON_PORTAL_DB_PASS', default="password")
PORTAL_DB_NAME = config('FALCON_PORTAL_DB_NAME', default="falcon_portal")

# -- uic db config --
UIC_DB_HOST = config('FALCON_UIC_DB_HOST', default="127.0.0.1")
UIC_DB_PORT = config('FALCON_UIC_DB_PORT', default=3306, cast=int)
UIC_DB_USER = config('FALCON_UIC_DB_USER', default="root")
UIC_DB_PASS = config('FALCON_UIC_DB_PASS', default="password")
UIC_DB_NAME = config('FALCON_UIC_DB_NAME', default="uic")
UIC_DB_TABLE_SESSION = 'session'

# -- app config --
DEBUG = config('FALCON_DEBUG', default=False, cast=bool)
SENTRY_DSN = config('FALCON_SENTRY_DSN', default='')
SECRET_KEY = config('FALCON_SECRET_KEY', default="4e.5tyg8-u9ioj")
SESSION_COOKIE_NAME = config('FALCON_SESSION_COOKIE_NAME', default="falcon-portal")
SESSION_COOKIE_DOMAIN = config('FALCON_SESSION_COOKIE_DOMAIN', default=None)
SITE_COOKIE = "open-falcon-ck"

URL_PORTAL = config('FALCON_URL_PORTAL', default="http://127.0.0.1:5050")
URL_DASHBOARD = config('FALCON_URL_DASHBOARD', default="http://127.0.0.1:8081")
URL_GRAFANA = config('FALCON_URL_GRAFANA', default="http://127.0.0.1:3000")
URL_ALARM = config('FALCON_URL_ALARM', default="http://127.0.0.1:9912")
URL_UIC = config('FALCON_URL_UIC', default="http://127.0.0.1:1234")
URL_QUERY = config('FALCON_URL_QUERY', default="http://127.0.0.1:9966")

# -- query config --
QUERY_ADDR = URL_QUERY

LOG_PATH = config('FALCON_LOG_DIR', default="/var/log/falcon-dashboard")

JSONCFG = {}

JSONCFG['shortcut'] = {}
JSONCFG['shortcut']['falconPortal'] = URL_PORTAL
JSONCFG['shortcut']['falconDashboard'] = URL_DASHBOARD
JSONCFG['shortcut']['grafanaDashboard'] = URL_GRAFANA
JSONCFG['shortcut']['falconAlarm'] = URL_ALARM
JSONCFG['shortcut']['falconUIC'] = URL_UIC

JSONCFG['redirectUrl'] = '{}/auth/login?callback={}'.format(URL_UIC, URL_DASHBOARD)

try:
    from .local_config import *
except:
    pass
