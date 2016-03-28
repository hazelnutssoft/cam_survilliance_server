#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time

class User(Model):
    __table__ = 'device'

    id = IntegerField(primary_key=True, default=next_id)
    location = StringField(ddl='varchar(50)')
    mac = StringField(ddl='varchar(50)')
    duration = IntegerField()
    created_at = FloatField(updatable=False, default=time.time)