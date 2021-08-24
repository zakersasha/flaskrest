from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy & Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    producer = db.Column(db.String(30))
    price = db.Column(db.Float)

    def __init__(self, name, producer, price):
        self.name = name
        self.producer = producer
        self.price = price


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'producer', 'price')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    producer = request.json['producer']
    price = request.json['price']

    new_product = Product(name, producer, price)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@app.route('/products', methods=['GET'])
def list_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)

    return jsonify(result)


@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)

    return product_schema.jsonify(product)


@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    producer = request.json['producer']
    price = request.json['price']

    product.name = name
    product.producer = producer
    product.price = price

    db.session.commit()

    return product_schema.jsonify(product)


@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
