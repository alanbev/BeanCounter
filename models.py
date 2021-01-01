import datetime
from app import db

class Stock_list(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String(100),unique =True)
    kitchen_stock = db.Column(db.Integer)
    garage_stock = db.Column(db.Integer)
    minimum_stock = db.Column(db.Integer)
    barcode = db.Column(db.Integer)
    transaction = db.relationship('Transactions', backref='stock_item',lazy=True)

 


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    action = db.Column(db.String)
    number_actioned = db.Column(db.Integer, nullable = False)
    date = db.Column(db.DateTime, default = datetime.datetime.now)
    item = db.Column(db.String, db.ForeignKey('stock_list.id'))


db.create_all()
