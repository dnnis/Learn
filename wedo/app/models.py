#/usr/bin/env python
#coding:utf-8
from app import db
from  datetime import datetime
from hashlib import md5
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),index=True,unique=True)
    email = db.Column(db.String(120),unique=True)
    nickname = db.Column(db.String(20),index=True,unique=True)
    password = db.Column(db.String(32), nullable=False)
    group_id= db.Column(db.Integer, db.ForeignKey('wgroup.id'))
    groupname = db.relationship('Wgroup',backref=db.backref('posts', lazy='dynamic'))
    last_seen = db.Column(db.DateTime)
    def __init__(self,username,email,nickname,groupname,password,last_seen=None):
        self.username=username
        self.email=email
        self.nickname=nickname
        self.groupname=groupname
        self.password=md5(password).hexdigest()
        if last_seen is None:
            last_seen=datetime.utcnow()
        self.last_seen=last_seen
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)
    def __repr__(self):
        return '<User %r>' % self.nickname
class Wgroup(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    group_name = db.Column(db.String(20),index=True,unique=True)
    def __init__(self, group_name):
        self.group_name = group_name
    def __repr__(self):
        return '<WGroup %r>' % self.group_name    
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(1200))
    posted_on = db.Column(db.DateTime )
    todo_begin = db.Column(db.DateTime )
    todo_end = db.Column(db.DateTime )
    status=db.Column(db.Integer,primary_key=True)
    pruduct_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    assign_group=db.relationship('Wgroup',backref=db.backref('assign', lazy='dynamic'))
    assign_group_id=db.Column(db.Integer, db.ForeignKey('wgroup.id'))
    do_user=db.relationship('User',backref=db.backref('douser', lazy='dynamic'))
    do_user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    Product = db.relationship('Product',backref=db.backref('product', lazy='dynamic'))
    
    def __init__(self,title,content,Product,assign_group,todo_begin=None,todo_end=None,do_user=None,status=0,posted_on=None):
        default_time=datetime.utcnow()
        self.title=title
        self.content=content
        self.Product=Product
        if todo_begin is None:
            todo_begin=default_time
        if todo_end is None:
            todo_end=default_time        
        self.todo_begin=todo_begin
        self.todo_end=todo_end
        self.status=status
        self.assign_group=assign_group
        self.do_user=do_user
        if posted_on is None:
            posted_on=default_time
        self.posted_on=posted_on
            
    def __repr__(self):
        return "<Todo '%s'>" % self.title    
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(255), index=True,unique=True)
    def __init__(self,product_name):
        self.product_name = product_name
    def __repr__(self):
        return "<Product '%s'>" % self.product_name  
