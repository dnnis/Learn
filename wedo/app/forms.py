#/usr/bin/env python
#coding:utf-8
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField,TextAreaField,PasswordField
from wtforms.validators import Required, Length

class LoginForm(Form):
    username=TextField('用户名',validators=[Required()])
    userpass=PasswordField('密码',validators=[Required()]))
    remeber_me=BooleanField(u"记住我",default=False)
