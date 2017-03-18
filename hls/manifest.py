from .protocol import *
from .segment import HLSSegment
from .parser import parse_hls

__all__ = ["HLSManifest"]

def mk_tag(key, value=False):
    result = key
    if value:
        result += ":" + str(value)
    return result + "\n"


class HLSManifest():
    def __init__(self, **kwargs):
        self.path_template = kwargs.get("path_template", "/media/{number}.ts")
        self.hls_version = kwargs.get("version", 3)
        self.url = kwargs.get("url", "/")
        self.segments = []
        self.duration = 0
        if kwargs.get("parse", False):
            parse_hls(self, kwargs["parse"])

    def add_segment(self, segment):
        segment.clip_time = self.duration
        self.segments.append(segment)
        self.duration += segment.duration
        return segment

    @property
    def media_sequence(self):
        return self.segments[0].media_sequence if self.segments else 0

    @property
    def target_duration(self):
        try:
            return max([segment.duration for segment in self.segments])
        except ValueError:
            return 0

    def render(self):
        result = "#EXTM3U\n"
        result+= mk_tag(ext_x_version, self.hls_version)
        result+= mk_tag(ext_x_media_sequence, self.media_sequence)
        result+= mk_tag(ext_x_targetduration, self.target_duration)
        for i, segment in enumerate(self.segments):
            if segment.is_first:
                result += mk_tag(ext_x_discontinuity)
            result += "#EXTINF:{},\n".format(segment.duration)
            result += segment.url or self.path_template.format(
                    number=self.media_sequence + i
                    )
            result += "\n"
        return result
