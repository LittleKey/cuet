#!/usr/bin/env python
# encoding: utf-8

import os


class Utils(object):

    @staticmethod
    def RecurMkdir(dirname):
        dirname = os.path.abspath(dirname)
        if not os.path.exists(dirname):
            Utils.RecurMkdir(os.path.dirname(dirname))
            os.mkdir(dirname)

if __name__ == '__main__':
    Utils.RecurMkdir('Hello/a/b/c')

