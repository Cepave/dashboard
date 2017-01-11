# -*- coding:utf-8 -*-

from werkzeug.contrib.fixers import ProxyFix
from rrd import create_app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
else:
    app.wsgi_app = ProxyFix(app.wsgi_app)
