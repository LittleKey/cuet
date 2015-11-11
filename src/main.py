#!/usr/bin/env python
# encoding: utf-8

import sys
import Cuet


if __name__ == '__main__':
    if (len(sys.argv)) == 2:
        cuet = Cuet.Cuet()
        cuet.openCue(sys.argv[1])
        for i in xrange(cuet.getTrackAmount()):
            cuet.cutMusic(*cuet.getMusicInfoByTrackIndex(i))

