from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form, TextField, SubmitField, required, ValidationError 
from  datetime import datetime
DEBUG=True
SECRET_KEY='f5\xd7w\xde\x01\xe8\xd0\x01\xb9\xcf0L\xde\x89cC\xbe\xd4\xd7\x02\x01\x03p'
SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.sqlite'
app=Flask(__name__)
db = SQLAlchemy(app)
db.init_app(app)
app.config.from_object(__name__)
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(255),nullable=False)
    posted_on=db.Column(db.Date,default=datetime.utcnow())
    status=db.Column(db.Boolean(),default=False)
    def __init__(self,*args,**kargs):
        super(Todo, self).__init__(*args,**kargs)
    def __repr__(self):
        return "<Todo '%s'>" % self.title
    def store_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete_todo(self):
        db.session.delete(self)
        db.session.commit()
        
    

if __name__ == '__main__':
    app.run()