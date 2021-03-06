#!/usr/bin/env python
# encoding: utf-8

import os
import multiprocessing
try:
    import av
except ImportError:
    av = None
import AFormatDetermine
import Time
from Utils import Utils


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
        if self._media_container:
            return self._media_container.format.name

    def getName(self):
        if self._media_container:
            return self._media_container.name

    def setCodec(self, codec):
        if isinstance(codec, (str, unicode)):
            self._codec = codec

    def setStartTime(self, time):
        if isinstance(time, (Time.Time, None.__class__)):
            self._start_time = time

    def setEndTime(self, time):
        if isinstance(time, (Time.Time, None.__class__)):
            self._end_time = time

    def overwrite(self):
        self._overwrite = True

    def process(self, out_filename):
        Utils.RecurMkdir(os.path.dirname(out_filename))
        if not self._media_container or (not self._overwrite and os.path.exists(out_filename)):
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

    def processByFFmpeg(self, out_filename):
        if not self._media_container or (not self._overwrite and os.path.exists(out_filename)):
            return
        command = [self._ffmpeg, '-i "{}"'.format(self.getName()), '-vn', '-acodec {}'.format(self._codec)]
        if self._start_time:
            command.append('-ss {}'.format(self._start_time.getFFmpegTime()))
        if self._end_time:
            command.append('-to {}'.format(self._end_time.getFFmpegTime()))
        command.append('-f {}'.format(AFormatDetermine.AFormatDetermine(self).getFormat()))
        if self._overwrite:
            command.append('-y')
        command.append('"{}"'.format(out_filename))

        os.system(' '.join(command))


def ProcessFunc(task):
    p = multiprocessing.Process(target=task)
    p.start()


