#/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm,EditForm
from models import User, ROLE_USER, ROLE_ADMIN
from datetime import datetime
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remeber_me = False
    if 'remeber_me' in session:
        remeber_me = session['remeber_me']
        session.pop('remeber_me', None)
    login_user(user, remember = remeber_me)
    return redirect(request.args.get('next') or url_for('index'))
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen=datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
@app.route('/')
@app.route('/index')
def index():
    user = g.user    
    username={'nickname':'曹海峰'}
    post=[
    {
        'author':{'nickname':'jhon'},
        'body':'Beautiful day in Portland!'
        },
    {
        'author':{'nickname':'Susan'},
        'body':'The Avengers movie was so cool!'
        }    
    ]
    return render_template('index.html',title="曹海峰",user=user,post=post)
@app.route('/login',methods=['GET','POST'])
@oid.loginhandler
def login():
    
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        session['remeber_me'] = form.remeber_me.data
        
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',title='登录',form=form,providers = app.config['OPENID_PROVIDERS'])
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user=User.query.filter_by(nickname=nickname).first()
    if user==None:
        flash("没有发现该用户:"+nickname)
        return redirect(url_for('index'))
    post=[
        {'author':user,'body':'The Post #1'},
        {'author':user,'body':'The Post #2'}
    ]
    return render_template('user.html',user=user,posts=post)
@app.route('/edit',methods=['POST','GET'])
@login_required
def edit():
    form=EditForm()
    if form.validate_on_submit():
        g.user.nickname=form.nickname.data
        g.user.about_me=form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('您的资料已经变更')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html',form=form)
@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'),404
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('50x.html'), 500