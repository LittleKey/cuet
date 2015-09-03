#!/usr/bin/env python
# encoding: utf-8

import sys
import CueReader

class CueCuter(object):

    def __init__(self, reader):
        self._reader = reader

    def getTimeZone(self, index):
        tracks = self._reader[index:index + 2]
        start_time = None
        end_time = None
        if tracks:
            cur_track = tracks[0]
            start_time = cur_track.get('start_time')
            if (len(tracks) == 2):
                next_track = tracks[1]
                end_time = next_track.get('last_end_time')

        if not start_time:
            start_time = "00:00:00"
        if not end_time:
            end_time = "00:00:00"

        return (start_time, end_time)

    def getTitle(self, index):
        track = self._reader.getTrack(index)
        if track:
            title = track.get('title')
        if not title:
            title = 'no title'

        return title


def ConvertTimeForFFmpeg(time):
    minute, sec, micro = map(lambda t: int (t), time.split(':'))
    micro = micro * 100 / 60

    return "%02d:%02d.%02d" % (minute, sec, micro)

if __name__ == '__main__':
    reader = CueReader.CueReader()
    reader.parse(sys.argv[1])
    cuter = CueCuter(reader)
    print(cuter.getTimeZone(1))
    print(ConvertTimeForFFmpeg(cuter.getTimeZone(0)[1]))
    print(cuter.getTitle(1))

