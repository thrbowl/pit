# -*- coding: utf-8 -*-
from flask import jsonify, Flask
from werkzeug.utils import import_string

from pit.ext import db
from pit.exc import BaseError, UnknownError
from pit.utils.app_mange import register_papp

apps = [
    'pit.apps.shici',
]

exts = [
    'pit.ext.db',
]


def create_app():
    app = Flask(__name__)
    app.config.from_object('pit.settings')

    for ext in exts:
        ext = import_string(ext)
        ext.init_app(app)

    # for papp in apps:
    #     papp = import_string(papp)
    #     register_papp(papp, app=app, db=db)
    from pit.apps.shici.models import db
    from pit.apps.shici.views import bp
    app.register_blueprint(bp)

    @app.before_first_request
    def create_database():
        db.create_all()

    @app.errorhandler(Exception)
    def catch_exceptions(exc):
        if app.debug:
            import traceback
            traceback.print_exc()
        if not isinstance(exc, BaseError):
            exc = UnknownError(str(exc))
        return jsonify({
            'status': exc.status,
            'msg': exc.description,
            'data': None
        })

    @app.teardown_request
    def teardown_request(exc):
        if not db.session:
            return
        if exc:
            db.session.rollback()
        else:
            db.session.commit()
        db.session.remove()

    print(app.url_map)
    return app
