#!/usr/bin/env python

import os
import requests

from nxtools import *
from hls import *

test_url = "http://tranquility.immstudios.org/nxtv.m3u8"

if __name__ == "__main__":
    data = requests.get(test_url)
    manifest = HLSManifest(parse=data.content)

    print manifest.media_sequence

    for segment in manifest.segments:
        print segment.url, "({})".format(segment.duration)
    print os.path.split(test_url)[0]


