#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
import Cue
import CharDetermine

class CueReader(object):

    def __init__(self):
        self._path_dir = '.'
        self._init_data()

    def _init_data(self):
        self._data = Cue.Cue()

    def parse(self, filename):
        if not (os.path.exists(filename) and os.path.isfile(filename)):
            return
        self._path_dir = os.path.abspath(os.path.dirname(filename))
        self._init_data()
        with open(filename) as f:
            # remove utf-8 bom header
            if f.read(3) != '\xef\xbb\xbf':
                f.seek(0)
            chardet = CharDetermine.CharDetermine(['utf8', 'gbk'])
            for line in f:
                if not line.startswith(' '):
                    self._processLine(chardet.processChar(line).strip())
                else:
                    self._processChunk(chardet.processChar(line).strip())

    def _processChunk(self, line):
        track_info = line.split()
        if line.startswith('TRACK'):
            self._data.newTrack(int(track_info[1]) - 1)
        elif track_info[0] == 'INDEX':
            time = ' '.join(track_info[2:])
            if int(track_info[1]) == 0:
                self._data.addTrackLastEndTime(time)
            else:
                self._data.addTrackStartTime(time)
        elif track_info[0] == 'TITLE':
            title_match = re.compile(r'^"?(.*?)"?$')
            self._data.addTrackInfo(track_info[0], title_match.match(' '.join(track_info[1:])).groups()[0])
        else:
            self._data.addTrackInfo(track_info[0], ' '.join(track_info[1:]))

    def _processLine(self, line):
        if line.startswith('REM'):
            rem_info = line.split()[1:]
            self._data.addREM(rem_info[0], ' '.join(rem_info[1:]))
        elif line.startswith('TITLE'):
            self._data.setTitle(' '.join(line.split()[1:]))
        elif line.startswith('FILE'):
            file_info = ' '.join(line.split()[1:])
            match = re.compile(r'^"?(.*?)"?\s*([a-zA-Z]*)$')
            rlt = match.match(file_info)
            if rlt:
                self._data.setFile(*rlt.groups())

    def getTrack(self, index):
        return self._data.getTrack(index)

    def getFilename(self):
        return os.path.join(self._path_dir, self._data.getFilename())

    def __getitem__(self, index):
        return self._data.__getitem__(index)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)


if __name__ == '__main__':
    cue_filename = sys.argv[1]
    cue_reader = CueReader()
    cue_reader.parse(cue_filename)
    print(cue_reader)

