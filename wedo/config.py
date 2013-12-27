import os
basedir=os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_DATABASE_URI='mysql://wedo:wedo@localhost/wedo'
CSRF_ENABLED = True
SECRET_KEY = 'www.wedogame.com'