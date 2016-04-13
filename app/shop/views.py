#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json

from flask import send_from_directory, request, render_template
from sqlalchemy import desc, func

from . import shop_blueprint
from ..models import *

product_sort = {
    # 낮은 가격순
    'low': Product.query.filter(Product.name.contains(query)).order_by('price').all(),
    # 높은 가격순
    'high': Product.query.filter(Product.name.contains(query)).order_by(desc('price')).all(),
    # 인기도 순
    'popular': [p for p, cnt in
                db.session.query(Product, func.count(likes.c.person_id).label('like_total')).join(likes).group_by(
                    Product).filter(Product.name.contains(query)).order_by(desc('like_total')).all()]
}


@shop_blueprint.route('/list/json')
@shop_blueprint.route('/list/json/')
@shop_blueprint.route('/list/json/<string:query>')
def product_list_json(query=""):
    try:
        all_products = product_sort[request.args['sort']]
    except KeyError:
        all_products = product_sort['popular']

    data = []
    order = 0

    for product in all_products:
        data.append({
            'order': order + 1,
            'title': product.name,
            'image': [image.image for image in product.image],
            'writer': product.user.name,
            'price': product.price,
            'like': len(product.like),
            'comment': len(product.comment),
            'writer_img': product.user.image,
            'tags': [tag.name for tag in product.tag],
        })

        order += 1

    return json.dumps(data)


@shop_blueprint.route('/list')
@shop_blueprint.route('/list/')
@shop_blueprint.route('/list/<string:query>')
def product_list(query=""):
    product_sort = {
        # 낮은 가격순
        'low': Product.query.filter(Product.name.contains(query)).order_by('price').all(),
        # 높은 가격순
        'high': Product.query.filter(Product.name.contains(query)).order_by(desc('price')).all(),
        # 인기도 순
        'popular': [p for p, cnt in
                    db.session.query(Product, func.count(likes.c.person_id).label('like_total')).join(likes).group_by(
                        Product).filter(Product.name.contains(query)).order_by(desc('like_total')).all()]
    }

    try:
        all_products = product_sort[request.args['sort']]
    except KeyError:
        all_products = product_sort['popular']

    top_tag_list = Tag.query.filter_by(top=True).all()

    return render_template('shop/main.html',
                           all_products=all_products,
                           top_tag=top_tag_list)


@shop_blueprint.route('/image/<path:filename>')
def shop_image(filename):
    return send_from_directory(shop_blueprint.root_path + '/image/', filename)
