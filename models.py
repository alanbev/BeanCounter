import datetime
from app import db

class Stock_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100),unique=True)
    kitchen_stock = db.Column(db.Integer, default=0)
    garage_stock = db.Column(db.Integer, default=0)
    minimum_stock = db.Column(db.Integer,default=0)
    barcode = db.Column(db.Integer)
    to_buy = db.Column(db.Integer, default=0)
    transaction = db.relationship('Transactions', backref='stock_item',lazy=True)

 


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    action = db.Column(db.String)
    number_actioned = db.Column(db.Integer, nullable = False)
    date = db.Column(db.DateTime, default = datetime.datetime.now)
    item = db.Column(db.String, db.ForeignKey('stock_list.id'))


db.create_all()
