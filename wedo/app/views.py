#/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db,login_manager
from forms import LoginForm


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))
@app.route('/',methods=["GET", "POST"])
def index():
    form=LoginForm()
    if form.validate_on_submit():
        
    return render_template('index.html')