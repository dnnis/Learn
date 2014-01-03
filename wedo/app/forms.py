#/usr/bin/env python
#coding:utf-8
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField,TextAreaField,PasswordField,DateTimeField,SelectField
from wtforms.validators import Required, Length,ValidationError,InputRequired,DataRequired
from hashlib import md5

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
        
class UpdateTodo(Form):
    title=TextField('标题',validators=[Required()])
    content=TextAreaField("任务内容",validators=[Required()])
    post_user=TextField('发起人',validators=[Required()])
    todo_begin=DateTimeField(label="期望开始时间", validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    todo_end=DateTimeField(label="期望结束时间", validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    status=SelectField('状态',coerce=int)
    pruduct=SelectField('产品',coerce=int)
    assign_group=SelectField('处理团队',coerce=int)
    assign_user=SelectField('处理团队',coerce=int)
    