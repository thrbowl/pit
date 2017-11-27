# -*- coding: utf-8 -*-
# !/usr/bin/env python
from flask_script import Manager
from gunicorn.app.wsgiapp import WSGIApplication

from pit import create_app
from pit import db

app = create_app()

manager = Manager(app)


@manager.shell
def make_shell_context():
    """Run With shell context."""
    return {'app': app, 'db': db}


@manager.command
def runserver(host='0.0.0.0', port=8360, workers=1):
    """Run the app with Gunicorn."""

    if app.debug:
        app.run(host, int(port), use_reloader=False)
    else:
        gunicorn = WSGIApplication()
        gunicorn.load_wsgiapp = lambda: app
        gunicorn.cfg.set('bind', '%s:%s' % (host, port))
        gunicorn.cfg.set('workers', workers)
        gunicorn.cfg.set('pidfile', None)
        # gunicorn.cfg.set('worker_class', 'gunicorn.workers.ggevent.GeventWorker')
        gunicorn.cfg.set('accesslog', '-')
        gunicorn.cfg.set('errorlog', '-')
        gunicorn.cfg.set('timeout', 300)
        gunicorn.chdir()
        gunicorn.run()
