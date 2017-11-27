# -*- coding: utf-8 -*-
from pit.ext import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Article(db.Model):
    pass
