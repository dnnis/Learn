#/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db,models,login_manager
from forms import LoginForm
from hashlib import md5
from datetime import datetime


@login_manager.user_loader
def load_user(userid):
    return models.User.query.get(int(userid))
@app.route('/',methods=["GET", "POST"])
def index():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))    
    form=LoginForm()
    if form.validate_on_submit():
        session['remeber_me']=form.remeber_me.data
        user = db.session.query(models.User).filter_by(username=form.username.data).first()
        if user is None or md5(form.userpass.data).hexdigest() != user.password:
            flash("用户名或密码错误")
            return render_template('index.html',form=form)
        login_user(user)
        return redirect(url_for('home'))
    return render_template('index.html',form=form)
@app.route('/home')
@login_required
def home():
    user=g.user
    entries = models.Todo.query.order_by(models.Todo.id.desc())
    return render_template('/Dash/home.html',user=user,entries=entries)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/event/<int:event_id>/')
@app.route('/event/')
@login_required
def event():
    return render_template('/Dash/reports.html')
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen=datetime.utcnow()
