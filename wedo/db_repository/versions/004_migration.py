from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
todo = Table('todo', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=255), nullable=False),
    Column('content', String(length=1200)),
    Column('post_user_id', Integer),
    Column('posted_on', DateTime),
    Column('todo_begin', DateTime),
    Column('todo_end', DateTime),
    Column('status', Integer, primary_key=True, nullable=False),
    Column('pruduct_id', Integer),
    Column('assign_group_id', Integer),
    Column('do_user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['todo'].columns['post_user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['todo'].columns['post_user_id'].drop()
