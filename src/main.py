#!/usr/bin/env python
# encoding: utf-8

import sys
import Cuet


if __name__ == '__main__':
    argv = sys.argv
    out_dir = '.'
    if len(argv) == 3:
        out_dir = argv.pop()
    if len(argv) == 2:
        cuet = Cuet.Cuet()
        cuet.setOutDir(out_dir)
        cuet.openCue(sys.argv[1])
        for i in xrange(cuet.getTrackAmount()):
            cuet.cutMusic(*cuet.getMusicInfoByTrackIndex(i))

