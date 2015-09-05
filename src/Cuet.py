#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import CueCuter
import CueReader


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

    def cutMusicByFFmpeg(self, filename, title, start_time, end_time, audio_type='flac'):
        extname = os.path.splitext(filename)[-1]
        if end_time != '00:00.00':
            os.system('ffmpeg -i "{filename}" -vn -acodec flac -ss {start_time} -to {end_time} -f {audio_type} -y "{title}{extname}"'.format(
                filename=filename,
                start_time=start_time,
                end_time=end_time,
                audio_type=audio_type,
                title=title,
                extname=extname))
        else:
            os.system('ffmpeg -i "{filename}" -vn -acodec flac -ss {start_time} -f {audio_type} -y "{title}{extname}"'.format(
                filename=filename,
                start_time=start_time,
                audio_type=audio_type,
                title=title,
                extname=extname))

if __name__ == '__main__':
    cuet = Cuet()
    cuet.openCue(sys.argv[1])
    cuet.cutMusicByFFmpeg(*cuet.getMusicInfoByTrackNumber(1))
    print('finish.')

