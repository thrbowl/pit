# -*- coding: utf-8 -*-
from flask import jsonify, Flask
from werkzeug.utils import import_string

from pit.ext import db
from pit.exc import BaseError, UnknownError

blueprints = [
    'pit.apps.shici',
]

extensions = [
    'pit.ext.db',
]


def create_app():
    app = Flask(__name__)
    app.config.from_object('pit.settings')

    for ext in extensions:
        extension = import_string(ext)
        extension.init_app(app)

    # for blueprint in blueprints:
    #     blueprint = import_string(blueprint)
    #     app.register_blueprint(blueprint)

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

    return app
