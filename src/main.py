#!/usr/bin/env python
# encoding: utf-8

import sys
import Cuet


if __name__ == '__main__':
    if (len(sys.argv)) == 2:
        cuet = Cuet.Cuet()
        cuet.openCue(sys.argv[1])
        for i in range(len(cuet._reader)):
            cuet.cutMusic(*cuet.getMusicInfoByTrackNumber(i + 1))

