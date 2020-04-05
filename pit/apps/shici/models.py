# -*- coding: utf-8 -*-
from datetime import datetime

from pit.ext import db


class Article(db.Model):
    __tablename__ = 'apps_shici_article'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), nullable=False, index=True)
    dynasty = db.Column(db.String(32), nullable=False, index=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.TEXT)
    tags = db.Column(db.String(255))
    add_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
