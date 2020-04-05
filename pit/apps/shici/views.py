# -*- coding: utf-8 -*-
from flask import Blueprint, request
from flask import render_template
from .models import Article

bp = Blueprint(__name__, __package__, url_prefix='/apps/shici', template_folder='templates', static_folder='static')
print(bp.root_path)


@bp.route('')
def index():
    params = request.args
    page = int(params.get('page', 1))
    limit = int(params.get('limit', 20))
    author = params.get('author')
    dynasty = params.get('dynasty')
    title = params.get('title')

    query = Article.query
    if author:
        query = query.filter(Article.name == author)
    if dynasty:
        query = query.filter(Article.dynasty == dynasty)
    if title:
        title = title.replace("%", "\\%")
        query = query.filter(Article.title.like('%' + title + '%'))

    total = query.count()

    query = query.order_by(Article.add_time.asc())

    pagination = query.paginate(page, per_page=limit, error_out=False)
    rs = pagination.items
    results = [{
        'author': r.author,
        'dynasty': r.dynasty,
        'title': r.title,
        'content': r.content.replace('\n', '<br/>'),
        'tags': r.tags,
        'add_time': r.add_time.strftime("%Y-%m-%d %H:%M:%S"),
    } for r in rs]

    data = {
        'page': page,
        'limit': limit,
        'total': total,
        'results': results,
        'pager': pagination,
    }
    return render_template('apps/shici/index.html', **data)
