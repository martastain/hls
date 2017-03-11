from .segment import HLSSegment
from .parser import parse_hls

__all__ = ["HLSManifest"]

class HLSManifest():
    def __init__(self, **kwargs):
        self.path_template = kwargs.get("path_template", "/media/{number}.ts")
        self.hls_version = 3
        self.segments = []
        self.duration = 0
        self.url = kwargs.get("url", "/")

        if kwargs.get("parse", False):
            parse_hls(self, kwargs["parse"])

    def add_segment(self, segment):
        segment.clip_time = self.duration
        self.segments.append(segment)
        self.duration += segment.duration

    @property
    def media_sequence(self):
        if not self.segments:
            return 0
        return self.segments[0].media_sequence

    @property
    def target_duration(self):
        try:
            return max([segment.duration for segment in self.segments])
        except ValueError:
            return 0

    def render(self):
        result = "#EXTM3U\n"
        result+= "#EXT-X-VERSION:{}\n".format(self.hls_version)
        result+= "#EXT-X-MEDIA-SEQUENCE:{}\n".format(self.media_sequence)
        result+= "#EXT-X-TARGETDURATION:{}\n".format(self.target_duration)
        for i, segment in enumerate(self.segments):
            if segment.is_first:
                result += "#EXT-X-DISCONTINUITY\n"
            result += "#EXTINF:{},\n".format(segment.duration)
            result += self.path_template.format(
                    number=self.media_sequence + i
                    )
            result += "\n"
        return result

