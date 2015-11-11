#!/usr/bin/env python
# encoding: utf-8

import sys
import CueCuter
import CueReader
import AFormatDetermine
import AudioProcessor


class Cuet(object):

    def __init__(self):
        self._reader = CueReader.CueReader()
        self._cuter = CueCuter.CueCuter(self._reader)

    def openCue(self, filename):
        self._reader.parse(filename)

    def getMusicInfoByTrackNumber(self, index):
        index -= 1
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

        output_filename = '{title}{extname}'.format(title=title, extname=extname)
        if ap.getName().endswith('.ape'):
            ap.processByFFmpeg(output_filename)
        else:
            ap.process(output_filename)

    def getTrackAmount(self):
        return len(self._reader)

if __name__ == '__main__':
    cuet = Cuet()
    cuet.openCue(sys.argv[1])
    cuet.cutMusic(*cuet.getMusicInfoByTrackNumber(1))
    print('tracks amount: {}'.format(cuet.getTrackAmount()))
    print('finish.')

