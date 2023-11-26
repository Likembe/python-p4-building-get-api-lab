#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    data = [{'id': bakery.id, 'name': bakery.name, 'created_at': bakery.created_at} for bakery in bakeries]
    return jsonify(data)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': bakery.created_at
        } 
        
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    data = [
        {
            'id': bg.id, 
            'name': bg.name, 
            'price': bg.price,
            'created_at': bg.created_at  # Include 'created_at' field
        } 
        for bg in baked_goods
    ]
    return jsonify(data), 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        data = {
            'id': most_expensive.id, 
            'name': most_expensive.name, 
            'price': most_expensive.price,
            'created_at': most_expensive.created_at  # Include 'created_at' field
        }
        return jsonify(data), 200
    else:
        return jsonify({'error': 'No baked goods found'}), 404    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
