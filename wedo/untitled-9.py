#/usr/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from app import db,models
a=models.Wgroup(group_name='test',)