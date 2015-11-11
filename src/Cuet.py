#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import CueCuter
import CueReader
import AFormatDetermine
import AudioProcessor


class Cuet(object):

    def __init__(self):
        self._reader = CueReader.CueReader()
        self._cuter = CueCuter.CueCuter(self._reader)
        self._out_dirname = os.path.curdir

    def openCue(self, filename):
        self._reader.parse(filename)

    def getMusicInfoByTrackIndex(self, index):
        if len(self._reader) > index and index >= 0:
            filename = self._reader.getFilename()
            title = self._cuter.getTitle(index)
            start_time, end_time = self._cuter.getTimeZone(index)

            return (filename, title, start_time, end_time)

        return None

    def cutMusic(self, filename, title, start_time, end_time):
        ap = AudioProcessor.AudioProcessor()
        ap.open(filename)
        afdet = AFormatDetermine.AFormatDetermine(ap)
        coder = afdet.determineEncode()
        extname = afdet.getExtname()

        ap.setCodec(coder)
        ap.setStartTime(start_time)
        ap.setEndTime(end_time)
        ap.overwrite()

        output_filename = os.path.join(self._out_dirname,
                '{title}{extname}'.format(title=title, extname=extname))
        if ap.getName().endswith('.ape'):
            ap.processByFFmpeg(output_filename)
        else:
            ap.process(output_filename)

    def getTrackAmount(self):
        return len(self._reader)

    def setOutDir(self, dirname):
        if os.path.isdir(dirname):
            self._out_dirname = dirname

if __name__ == '__main__':
    cuet = Cuet()
    cuet.openCue(sys.argv[1])
    cuet.cutMusic(*cuet.getMusicInfoByTrackIndex(0))
    print('tracks amount: {}'.format(cuet.getTrackAmount()))
    print('finish.')

