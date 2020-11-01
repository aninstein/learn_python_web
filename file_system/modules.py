#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid


from sqlalchemy import Column, Integer, String, DateTime
from ext import db


class PasteFile(db.Model):
    __tablename__ = 'PasteFile'
    id = Column(Integer, primary_key=True)
    filename = Column(String(5000), nullable=False)
    filehash = Column(String(128), nullable=False, unique=True)
    filemd5 = Column(String(128), nullable=False, unique=True)
    uploadtime = Column(DateTime, nullable=False)
    mimetype = Column(String(256), nullable=False)
    size = Column(Integer, nullable=False)

    def __init__(self):
        pass

    @staticmethod
    def hash_filename(filename):
        _, _, suffix = filename.rpartition('.')
        return '%s.%s' % (uuid.uuid4().hex, suffix)
