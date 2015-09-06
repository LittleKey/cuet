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
            start_time = cur_track.start_time
            if (len(tracks) == 2):
                next_track = tracks[1]
                try:
                    end_time = next_track.last_end_time
                except AttributeError:
                    end_time = next_track.start_time

        return (start_time, end_time)

    def getTitle(self, index):
        track = self._reader.getTrack(index)
        if track:
            title = track.title
        if not title:
            title = 'no title'

        return title

if __name__ == '__main__':
    reader = CueReader.CueReader()
    reader.parse(sys.argv[1])
    cuter = CueCuter(reader)
    print(cuter.getTimeZone(1))
    print(cuter.getTimeZone(0)[1])
    print(cuter.getTitle(1))

