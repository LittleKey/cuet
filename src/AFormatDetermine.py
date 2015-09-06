#!/usr/bin/env python
# encoding: utf-8

import os
import AudioProcessor


class AFormatDetermine(object):

    _mapFormat2Encode = {
            'flac': 'flac',
            'wav': 'pcm_s16le'}

    _mapFormat2Extname = {
            'flac': '.flac',
            'wav': '.wav'}

    def __init__(self, filename, defalt_format='wav'):
        self._ap = AudioProcessor.AudioProcessor()
        self._ap.open(filename)
        self._default_format = defalt_format

    def canCopy(self):
        return self._ap.getFormat() in AFormatDetermine._mapFormat2Encode

    def determineEncode(self):
        if self.canCopy():
            return 'copy'
        return self._mapFormat2Encode.get(self.getFormat())

    def getFormat(self):
        return AFormatDetermine._mapFormat2Encode.get(self._ap.getFormat(),
                self._default_format)

    def getExtname(self):
        if self.canCopy():
            return os.path.splitext(self._ap.getName())[-1]
        return AFormatDetermine._mapFormat2Extname.get(self._default_format)

