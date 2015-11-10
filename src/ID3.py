#!/usr/bin/env python
# encoding: utf-8

try:
    from mutagen.easyid3 import EasyID3 as EasyID3
except ImportError:
    EasyID3 = None

class ID3(object):

    def __init__(self, filename, media_format='mp3'):
        if media_format == 'mp3' and EasyID3 != None:
            self._music = EasyID3(filename)
        else:
            self._music = None

    def isSupport(self):
        return self._music != None

    def keys(self):
        return self._music.keys()

    def save(self):
        self._music.save()

    def __getitem__(self, key):
        if key == 'cover':
            return None
        value = ' '.join(self._music[key])
        try:
            return ID3._convertToUTF8(value)
        except ValueError:
            return value

    def __setitem__(self, key, value):
        if key == 'cover':
            return;
        self._music[key] = [value]

    @classmethod
    def _convertToUTF8(cls, s):
        return ''.join(map(lambda ns: chr(ord(ns)), s)).decode('gbk')

if __name__ == '__main__':
    id3 = ID3('/Users/littlekey/Downloads/Friendship - 冈崎律子.mp3')
    print('support modify id3? {}'.format(id3.isSupport() and 'yes' or 'no'))
    print(id3['artist'])

