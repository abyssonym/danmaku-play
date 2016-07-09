#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from sys import argv
from subprocess import call, check_output, STDOUT
from danmaku2ass.danmaku2ass import Danmaku2ASS


ALPHA = 0.5
FPS = 60
resolution_matcher = re.compile("Video: [^\n]*, (\d\d\d+)x(\d\d\d+)\D")


def generate_ass(filename, xmlfile=None):
    if xmlfile is None:
        xmlfile = filename + ".xml"
    subsfile = filename.rsplit(".", 1)[0] + ".ass"
    cmd = ["ffprobe", filename]
    s = str(check_output(cmd, stderr=STDOUT))
    match = resolution_matcher.search(s)
    if not match:
        raise Exception("Could not determine display resolution for %s" % filename)
    width, height = int(match.group(1)), int(match.group(2))
    Danmaku2ASS(xmlfile, subsfile, width, height, text_opacity=ALPHA)
    return subsfile


def play(filename, subs=None):
    if subs is None:
        subs = generate_ass(filename)
    cmd = 'ffmpeg -i "%s" -r %s -vcodec libx264 -tune zerolatency -crf 18 -f mpeg - | mpv - --sub-file "%s"' % (filename, FPS, subs)
    call(cmd, shell=True)


if __name__ == "__main__":
    for filename in argv[1:]:
        play(filename)
