#/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db,models,login_manager
from forms import LoginForm,UpdateTodo
from hashlib import md5
from datetime import datetime
from flask.ext.babel import gettext

@app.template_filter('dateformat')
def dateformate(time):
    return time.strftime('%Y-%m-%d')
@app.template_filter('timeformat')
def timeformate(time):
    return time.strftime('%H:%M:%S')

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
@app.route('/home/')
@login_required
def home():
    user=g.user
    entries = models.Todo.query.order_by(models.Todo.id.desc())
      
    return render_template('/Dash/home.html',user=user,entries=entries)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/event/',methods=["GET", "POST"])
@app.route('/event/<event_id>/',methods=["GET", "POST"])
@login_required
def event(event_id=None):
    user=g.user
    if event_id is None:
        return redirect(url_for('home'))
    entry=models.Todo.query.filter_by(id=event_id).first()
    form=UpdateTodo()
    if request.method == 'POST': 
        if request.form['btn'] == '保存':
            if form.validate_on_submit():
                entry.title=form.title.data
                entry.content=form.content.data
                entry.Product=form.product.data
                entry.assign_group= form.assign_group.data
                entry.todo_begin=form.todo_begin.data
                entry.todo_end=form.todo_end.data
                entry.status=form.status.data
                entry.do_user=form.do_user.data
                db.session.commit()
                return redirect(url_for('home'))
        if request.form['btn'] == '处理':
            entry.status=1
            entry.do_user=user
            db.session.commit()
            return redirect(url_for('event',event_id=event_id))
        else:
            return redirect(url_for('home'))
    else:
        form.product.data=entry.Product
        form.title.data=entry.title
        form.content.data=entry.content
        form.post_on.data=entry.posted_on
        form.assign_group.data=entry.assign_group
        form.todo_begin.data=entry.todo_begin
        form.todo_end.data=entry.todo_end
        form.status.data=entry.status
        form.post_user.data=entry.post_user
        form.do_user.data=entry.do_user
        return render_template('/Dash/event.html',user=user,form=form)
@app.route('/create/',methods=["GET", "POST"])
@login_required
def create_todo():
    user=g.user
    if request.method == 'POST':
        form = UpdateTodo(request.form)
        if request.form['btn'] == '保存':
            
        
            if form.validate_on_submit():
                title=form.title.data
                content=form.content.data
                posted_on=datetime.now()
                product=form.product.data
                assign_group= form.assign_group.data
                todo_begin=form.todo_begin.data
                todo_end=form.todo_end.data
                status=form.status.data
                
                
                todo=models.Todo(title=title,content=content,Product=product,assign_group=assign_group,post_user=user,todo_begin=todo_begin,todo_end=todo_end,status=status)
                db.session.add(todo)
                db.session.commit()
                return redirect(url_for('home'))
            else:
                return render_template('/Dash/edit.html', user=user,form = form,)
        else:
            return redirect(url_for('home'))
        
    
    return render_template('/Dash/edit.html',user=user,form=UpdateTodo())

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen=datetime.now()

@app.route('/delete/<event_id>/',methods=["GET", "POST"])
@login_required
def delete(event_id):
    entry=models.Todo.query.filter_by(id=event_id).first()
    db.session.delete(entry)
    db.session.commit()
    flash('任务号:%s删除成功' % entry.id)
    return redirect(url_for('home'))