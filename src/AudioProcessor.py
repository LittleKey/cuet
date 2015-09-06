#!/usr/bin/env python
# encoding: utf-8

import av


class AudioProcessor(object):

    def __init__(self, ffmpeg='ffmpeg'):
        self._ffmpeg = ffmpeg

    def open(self, filename):
        self._media_container = av.open(filename)

    def getFormat(self):
        return self._media_container.format.name

    def getName(self):
        return self._media_container.name

