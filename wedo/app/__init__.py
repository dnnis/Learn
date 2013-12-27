#/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask.ext.login import LoginManager
from flask import Flask
from flask.ext.sqlalchemy import  SQLAlchemy
from flask.ext.login import LoginManager
app=Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.setup_app(app)
from app import models,views