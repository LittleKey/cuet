#!/usr/bin/env python
# encoding: utf-8

import Time


class Track(object):

    def __init__(self, index):
        self.index = index
        self._data = {}

    def addLastEndTime(self, time):
        t = Time.Time()
        t.parse(time)
        self._data['last_end_time'] = t

    def addStartTime(self, time):
        t = Time.Time()
        t.parse(time)
        self._data['start_time'] = t

    def addInfo(self, name, value):
        self._data[name.lower()] = value

    def getIndex(self):
        return self.index

    def __repr__(self):
        return repr(self._data)

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError("'{}' object has no attribute '{}'".format(Track.__name__, name))

