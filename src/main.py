#!/usr/bin/env python
# encoding: utf-8

import sys
import Cuet


if __name__ == '__main__':
    cuet = Cuet.Cuet()
    cuet.openCue(sys.argv[1])
    for i in range(len(cuet._reader)):
        cuet.cutMusicByFFmpeg(*cuet.getMusicInfoByTrackNumber(i + 1))

