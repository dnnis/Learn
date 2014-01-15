#/usr/bin/env python
#coding:utf-8
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField,TextAreaField,PasswordField,DateTimeField,SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length,ValidationError,InputRequired,DataRequired
from hashlib import md5
from app import models

class LoginForm(Form):
    username=TextField('用户名')
    userpass=PasswordField('密码')
    remeber_me=BooleanField("记住我",default=True)
    def validate_username(self, field):
        if len(field.data) == 0:
            raise ValidationError("用户名不得为空")
        
    def validate_userpass(self, field):
        if len(field.data) == 0:
            raise ValidationError("密码不得为空")   
  
def select_product():
    return models.Product.query
def select_group():
    return models.Wgroup.query
def select_user():
    return models.User.query
class UpdateTodo(Form):
    title=TextField('标题',validators=[Required()])
    content=TextAreaField("任务内容",validators=[Required()])
    post_user=QuerySelectField('提单人',query_factory=select_user,get_pk=lambda a: a.id,get_label= lambda a: a.nickname,allow_blank=True,blank_text='请选择')
    do_user=QuerySelectField('操作人',query_factory=select_user,get_pk=lambda a: a.id,get_label= lambda a: a.nickname,allow_blank=True,blank_text='请选择')
    post_on=DateTimeField(label="期望开始时间", format='%Y-%m-%d %H:%M:%S')
    todo_begin=DateTimeField(label="期望开始时间", format='%Y-%m-%d %H:%M:%S',validators=[Required()])
    todo_end=DateTimeField(label="期望结束时间", format='%Y-%m-%d %H:%M:%S',validators=[Required()])
    status=SelectField('状态',coerce=int,choices=[(0,'新建'),(1,'处理中'),(2,'完成'),(3,'暂停')])
    product=QuerySelectField('产品',query_factory=select_product,get_pk=lambda a: a.id,get_label= lambda a: a.product_name)
    assign_group=QuerySelectField('处理团队',query_factory=select_group,get_pk=lambda a: a.id,get_label= lambda a: a.group_name)

    