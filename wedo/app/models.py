#/usr/bin/env python
#coding:utf-8
from app import db
from  datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),index=True,unique=True)
    email = db.Column(db.String(120),unique=True)
    nickname = db.Column(db.String(20),index=True,unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('rolegroup.id'))
    group = db.relationship('rolegroup',backref='groupname',lazy='dynamic')
    last_seen = db.Column(db.DateTime)
    def __repr__(self):
        return '<User %r>' % self.nickname
class Wgroup(db.Model):
    __tablename__ = 'rolegroup'
    id = db.Column(db.Integer,primary_key=True)
    group_name = db.Column(db.String(20),index=True,unique=True)
    
    def __repr__(self):
        return '<WGroup %r>' % self.group_name    
    
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(1200))
    posted_on = db.Column(db.Date, default=datetime.utcnow)
    todo_begin = db.Column(db.Date, default=datetime.utcnow)
    todo_end = db.Column(db.Date, default=datetime.utcnow)
    status=db.Column(db.Integer,primary_key=True)
    pruduct_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    Product = db.relationship('Product',backref='product',lazy='dynamic')
    def __repr__(self):
        return "<Todo '%s'>" % self.title    
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    product = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return "<Product '%s'>" % self.product    
if __name__ == "__main__":
    db.drop_all()