# -*- coding: utf-8 -*-
from os.path import dirname, join
from collective.noticeboard import tests


def getData(filename):
    filename = join(dirname(tests.__file__), filename)
    return open(filename, 'rb').read()
