#!/usr/bin/env python
# encoding: utf-8

class AFormatDetermine(object):

    _mapFormat2Encode = {
            'wav': 'pcm_s16le'}

    _mapFormat2Extname = {
            'wav': '.wav'}

    def __init__(self, audioProcessor, defalt_format='wav'):
        self._ap = audioProcessor
        self._default_format = defalt_format

    def determineEncode(self):
        return self._mapFormat2Encode.get(self.getFormat())

    def getFormat(self):
        return AFormatDetermine._mapFormat2Encode.get(self._ap.getFormat(),
                self._default_format)

    def getExtname(self):
        return AFormatDetermine._mapFormat2Extname.get(self.getFormat())

