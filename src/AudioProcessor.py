#!/usr/bin/env python
# encoding: utf-8

import os
import multiprocessing
import av


class AudioProcessor(object):

    def __init__(self, ffmpeg='ffmpeg'):
        self._ffmpeg = ffmpeg
        self._codec = 'pcm_s16le'
        self._media_container = None
        self._overwrite = False

    def open(self, filename):
        if os.path.isfile(filename):
            self._media_container = av.open(filename)

    def getFormat(self):
        return self._media_container.format.name

    def getName(self):
        return self._media_container.name

    def setCodec(self, codec):
        self._codec = codec

    def setStartTime(self, time):
        self._start_time = time

    def setEndTime(self, time):
        self._end_time = time

    def overwrite(self):
        self._overwrite = True

    def process(self, out_filename):
        if not self._overwrite and os.path.exists(out_filename):
            return
        output_container = av.open(out_filename, 'w')
        input_audio_stream = next(s for s in self._media_container.streams if s.type == b'audio')

        output_audio_stream = output_container.add_stream(self._codec, input_audio_stream.rate)

        start_time = self._start_time and self._start_time.getFFmpegTime()
        end_time = self._end_time and self._end_time.getFFmpegTime()
        packet_list = self._media_container.demux(input_audio_stream)
        def task():
            print("processing '{}'".format(out_filename))
            for packet in packet_list:
                for frame in packet.decode():
                    if start_time and frame.time < start_time:
                        continue
                    if end_time and end_time < frame.time:
                        break
                    output_container.mux(output_audio_stream.encode(frame))
            output_container.close()
            print("processed '{}'".format(out_filename))
        ProcessFunc(task)


def ProcessFunc(task):
    p = multiprocessing.Process(target=task)
    p.start()


