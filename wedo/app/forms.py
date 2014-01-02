#/usr/bin/env python
#coding:utf-8
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField,TextAreaField,PasswordField
from wtforms.validators import Required, Length,ValidationError,InputRequired
from hashlib import md5

class LoginForm(Form):
    username=TextField('用户名')
    userpass=PasswordField('密码')
    remeber_me=BooleanField("记住我",default=False)
    def validate_username(self, field):
        if len(field.data) == 0:
            raise ValidationError("用户名不得为空")
        
    def validate_userpass(self, field):
        if len(field.data) == 0:
            raise ValidationError("密码不得为空")    
        
