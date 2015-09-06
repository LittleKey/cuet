#!/usr/bin/env python
# encoding: utf-8

class Time(object):

    def __init__(self, hour=0, minute=0, sec=0, micro=0):
        self._hour = hour
        self._minute = minute
        self._sec = sec
        self._micro = micro

    def parse(self, time):
        if isinstance(time, (str, unicode)):
            minute, sec, micro = map(lambda t: int(t), time.split(':'))
            self._minute = minute
            self._sec = sec
            self._micro = micro * 1000 / 60

    def toMicroSec(self):
        return (self._minute * 60 + self._sec) * 1000 + self._micro

    def getFFmpegTime(self):
        return self.toMicroSec() / 1000.0

    def __eq__(self, other):
        if isinstance(other, Time):
            return self.toMicroSec() == self.toMicroSec()
        elif isinstance(other, (int, float)):
            return self.toMicroSec() == other
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __cmp__(self, other):
        if isinstance(other, Time):
            return self.toMicroSec() - other.toMicroSec()
        elif isinstance(other, (int, float)):
            return self.toMicroSec() - other
        else:
            raise ValueError("no support compare with '{}'".format(other))

    def __repr__(self):
        return '%02d:%02d:%02d:%03d' % (self._hour, self._minute, self._sec, self._micro)

