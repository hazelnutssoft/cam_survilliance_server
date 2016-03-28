# coding=utf-8
import os,sys
from celery import Celery,platforms
import json
import time
from model import user

reload(sys)
sys.setdefaultencoding( "utf-8" )

celery = Celery("tasks", broker="amqp://")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')

platforms.C_FORCE_ROOT = True

@celery.task(name='handler.tasks.user_login')
def user_login(username, password):
    u = user.User.find_first('where name = ? and password = ?',username, password)
    if u:
        return u.id