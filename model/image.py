#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time

class Image(Model):
    __table__ = 'image'

    id = IntegerField(primary_key=True, default=next_id)
    path = StringField(ddl='varchar(50)')
    created_at = FloatField(updatable=False, default=time.time)