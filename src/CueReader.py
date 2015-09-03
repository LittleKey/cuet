#!/usr/bin/env python
# encoding: utf-8

import sys
import re

class CueReader(object):

    def __init__(self):
        self._init_data()

    def _init_data(self):
        self._data = {
                'rem': {},
                'title': '',
                'file': ['', ''],
                'tracks': []
                }

    def parse(self, filename):
        self._init_data()
        with open(filename) as f:
            # remove utf-8 bom header
            if f.read(3) != '\xef\xbb\xbf':
                f.seek(0)
            for line in f:
                if not line.startswith(' '):
                    self._processLine(line.strip())
                else:
                    self._processChunk(line.strip())

    def _processChunk(self, line):
        is_new_chunk = line.startswith('TRACK')
        if is_new_chunk:
            self._saveTrackInfo('number', line.split()[1])
        else:
            track_info = line.split()
            self._saveTrackInfo(track_info[0], ' '.join(track_info[1:]))

    def _processLine(self, line):
        if line.startswith('REM'):
            rem_info = line.split()[1:]
            self._saveREMInfo(rem_info[0], ' '.join(rem_info[1:]))
        elif line.startswith('TITLE'):
            title_info = ' '.join(line.split()[1:])
            self._saveTitleInfo(title_info)
        elif line.startswith('FILE'):
            file_info = ' '.join(line.split()[1:])
            match = re.compile(r'"(.*)\"\s*([a-zA-Z]*)')
            rlt = match.match(file_info)
            if rlt:
                self._saveFileInfo(*rlt.groups())

    def _saveTrackInfo(self, name, value):
        if name == 'number':
            self._data['tracks'].insert(int(value) - 1, {})
        elif name == 'INDEX':
            num, time = value.split()
            index_name = int(num) == 0 and 'last_end_time' or 'start_time'
            self._data['tracks'][-1][index_name] = time
        else:
            self._data['tracks'][-1][name.lower()] = value

    def _saveREMInfo(self, name, value):
        self._data['rem'][name] = value

    def _saveTitleInfo(self, title):
        self._data['title'] = title

    def _saveFileInfo(self, filename, filetype):
        self._data['file'] = [filename, filetype]

    def get(self, index, default=None):
        if len(self) > index:
            return self._data[index]
        return default

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            return [self.get(i) for i in range(*indices)]
        else:
            return self.get(index)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)


if __name__ == '__main__':
    cue_filename = sys.argv[1]
    cue_reader = CueReader()
    cue_reader.parse(cue_filename)
    print(cue_reader)

