class HLSSegment():
    def __init__(self, manifest, **kwargs):
        self.manifest = manifest
        self.meta = kwargs
        self.clip_time = 0

    def __repr__(self):
        return "HLS Segment {}".format(self.media_sequence)

    @property
    def number(self):
        return self.meta.get("number", 0)

    @property
    def media_sequence(self):
        return self.meta.get("media_sequence", self.number)

    @property
    def duration(self):
        return self.meta.get("duration", 0)

    @property
    def is_first(self):
        return self.meta.get("is_first", self.number == 0)

    @property
    def url(self):
        return self.meta.get("url", False)
