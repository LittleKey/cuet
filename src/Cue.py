#!/usr/bin/env python
# encoding: utf-8


class Cue(object):

    def __init__(self):
        self._data = {
                'rem': {},
                'title': '',
                'file': ['', ''],
                'tracks': [],
                }

    def newTrack(self, index):
        self._data['tracks'].insert(index, {})

    def addTrackLastEndTime(self, time):
        self._data['tracks'][-1]['last_end_time'] = time

    def addTrackStartTime(self, time):
        self._data['tracks'][-1]['start_time'] = time

    def addTrack(self, name, value):
        self._data['tracks'][-1][name.lower()] = value

    def addREM(self, name, value):
        self._data['rem'][name.lower()] = value

    def setTitle(self, title):
        self._data['title'] = title

    def setFile(self, filename, filetype):
        self._data['file'] = [filename, filetype]

    def getTrack(self, index):
        if len(self) > index:
            return self._data['tracks'][index]
        raise IndexError("out of index range")

    def getFilename(self):
        if len(self._data['file']) == 2:
            return self._data['file'][0]
        return ''

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            return [self.getTrack(i) for i in range(*indices)]
        else:
            return self.getTrack(index)

    def __len__(self):
        return len(self._data['tracks'])

    def __repr__(self):
        return repr(self._data)

