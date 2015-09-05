#!/usr/bin/env python
# encoding: utf-8

class AFormatDetermine(object):

    _mapFormat2Encode = {
            'flac': 'flac',
            'wav': 'pcm_s16le'}

    _mapExtname2Format = {
            '.flac': 'flac',
            '.wav': 'wav'}

    @classmethod
    def canCopy(cls, extname):
        return cls.extname2format(extname) != None

    @classmethod
    def determineEncode(cls, extname):
        return cls._mapFormat2Encode.get(cls.extname2format(extname))

    @classmethod
    def extname2format(cls, extname):
        return cls._mapExtname2Format.get(extname)
