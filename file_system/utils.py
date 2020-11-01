#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


def get_file_md5(file_path):
    """
    返回文件的md5
    :return:
    """
    m = hashlib.md5()
    with open(file_path,'rb') as f:
        for line in f:
            m.update(line)
    md5code = m.hexdigest()
    print(md5code)
    return md5code


def humanize_bytes(byte_len):
    """
    返回可读的文件大小
    :return:
    """
    kb = 1024
    mb = kb * kb
    gb = mb * kb
    if byte_len < 1024:
        return '%s B' % byte_len
    elif kb <= byte_len < mb:
        return '%s KB' % round(float(byte_len / kb), 2)
    elif mb <= byte_len < gb:
        return '%s MB' % round(float(byte_len / mb), 2)
    elif gb <= byte_len:
        return '%s GB' % round(float(byte_len / gb), 2)
    else:
        raise Exception()


def get_file_path():
    """
    返回上传文件的目录获得文件路径
    :return:
    """
    return ""


if __name__ == '__main__':
    print(humanize_bytes(10000000000))
