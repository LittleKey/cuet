#!/usr/bin/env python
# encoding: utf-8

class Time(object):

    @staticmethod
    def parse_from_ms(time):
        """@param time must be int and unit is microsecond"""
        if isinstance(time, (int,)) and time >= 0:
            micro = time % 1000
            src = (time / 1000) % 60
            minute = time / (1000 * 60)
            return Time(minute, src, micro)

    def __init__(self, minute=0, sec=0, micro=0):
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

    def __sub__(self, right):
        if isinstance(right, Time):
            return Time.parse_from_ms(self.toMicroSec() - right.toMicroSec())
        elif isinstance(right, int):
            return Time.parse_from_ms(self.toMicroSec() - right)
        else:
            raise TypeError("unsupported operand type(s) for -: '{}' and '{}'".format(
                type(self), type(right)))

    def __add__(self, right):
        if isinstance(right, Time):
            return Time.parse_from_ms(self.toMicroSec() + right.toMicroSec())
        elif isinstance(right, int):
            return Time.parse_from_ms(self.toMicroSec() + right)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(
                type(self), type(right)))

    def __repr__(self):
        return '%02d:%02d:%03d' % (self._minute, self._sec, self._micro)

