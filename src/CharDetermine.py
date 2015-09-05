#!/usr/bin/env python
# encoding: utf-8

class CharDetermine(object):

    def __init__(self, decode_list):
        self._decode_list_iter = iter(decode_list)
        self._nextEncode()

    def _nextEncode(self):
        try:
            self._current_decode = self._decode_list_iter.next()
        except StopIteration:
            raise IndexError("'{}' no more decode".format(self))

    def processChar(self, chars):
        while (True):
            try:
                return chars.decode(self._current_decode).encode('utf8')
            except UnicodeDecodeError:
                self._nextEncode()
                continue
            except IndexError:
                raise UnicodeDecodeError("'{}' can't decode '{}'".format(self, chars))


