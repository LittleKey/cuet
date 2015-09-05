#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import CueCuter
import CueReader
import AFormatDetermine


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
            start_time, end_time = map(lambda t: CueCuter.ConvertTimeForFFmpeg(t),
                    self._cuter.getTimeZone(index))

            return (filename, title, start_time, end_time)

        return None

    def cutMusicByFFmpeg(self, filename, title, start_time, end_time):
        # TODO : 集成ffmpeg
        extname = os.path.splitext(filename)[-1]
        afdet = AFormatDetermine.AFormatDetermine()
        coder = 'copy'
        if not afdet.canCopy(extname):
            extname = '.wav'
            coder = afdet.determineEncode(extname)
        output_format = afdet.extname2format(extname)

        if end_time != '00:00.00':
            os.system('ffmpeg -i "{filename}" -vn -acodec {coder} -ss {start_time} -to {end_time} -f {output_format} "{title}{extname}"'.format(
                filename=filename,
                coder=coder,
                start_time=start_time,
                end_time=end_time,
                output_format=output_format,
                title=title,
                extname=extname))
        else:
            os.system('ffmpeg -i "{filename}" -vn -acodec {coder} -ss {start_time} -f {output_format} "{title}{extname}"'.format(
                filename=filename,
                coder=coder,
                start_time=start_time,
                output_format=output_format,
                title=title,
                extname=extname))

if __name__ == '__main__':
    cuet = Cuet()
    cuet.openCue(sys.argv[1])
    cuet.cutMusicByFFmpeg(*cuet.getMusicInfoByTrackNumber(1))
    print('finish.')

