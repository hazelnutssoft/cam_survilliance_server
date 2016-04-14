# coding=utf-8
import os,sys
#from celery import Celery,platforms
import json
import time
from model import user
from model.device import Device
from model.position import Position
from model.image import Image
from model.device_observed import Device_Observed
from util import getPWDDir
from util.marcos import *
from util import hash_password

#reload(sys)
#sys.setdefaultencoding( "utf-8" )

#celery = Celery("tasks", broker="amqp://")
#celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')

#platforms.C_FORCE_ROOT = True

#@celery.task(name='handler.tasks.user_login')
def user_login(username, password):
    u = user.User.find_first('where name = ? and password = ?', username, hash_password(password))
    if u:
        return u.id
    else:
        return None

#@celery.task(name='handler.tasks.img_upload')
def img_upload(device_mac, device_pos, meta):
    if device_mac == "":
        return False

    if device_pos == "":
        return False
    dev = Device()
    pos = Position()
    device_id = dev.get_device_by_mac(device_mac)
    position_id = pos.get_position_id(device_id, device_pos)

    upload_path = os.path.join(getPWDDir(), CAPTURED_DIR)
    filename = meta['filename']
    filename = os.path.basename(filename)
    print filename,'----',upload_path
    filepath = os.path.join(upload_path, filename)
    with open(filepath, 'wb') as up:
        up.write(meta['body'])
    img = Image()
    img.path = filepath
    img.position_id = position_id
    img_id = img.create()
    if not img_id:
        return False
    return True

#@celery.task(name='handler.tasks.get_summery_info')
def get_summery_info(user):
    dev_observed = Device_Observed()
    res = {'user_name': user.name, 'device_counts': dev_observed.count_user_devices(user.id), 'device_info': []}
    devices = dev_observed.observed_devices(user.id)

    pos = Position()
    for dev in devices:
        contents_dev = {}
        contents_dev['location'] = dev.location
        contents_dev['position_contents'] = []
        positions = pos.get_position_by_device_id(dev.id)
        if positions:
            for pos in positions:
                img = Image()
                image_count = img.count_by('where position_id = ?', pos.id)
                contents_dev['position_contents'].append({'position': pos.position,
                                                          'duration': pos.duration,
                                                          'image_count': image_count,
                                                          'object_name': pos.object_name})
        res['device_info'].append(contents_dev)

    return res
