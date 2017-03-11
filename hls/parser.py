import protocol
from .segment import HLSSegment

__all__ = ["parse_hls"]

def split_lines(text):
    return text.strip().replace("\r\n", "\n").split("\n")

def parse_hls(manifest, data):
    media_sequence = 0
    lines = split_lines(data)
    for i, line in enumerate(lines):
        line = line.strip()

        if line.startswith(protocol.ext_x_media_sequence):
            media_sequence = int(line.split(":")[1])

        elif line.startswith(protocol.extinf):
            segment = HLSSegment(
                    manifest,
                    media_sequence=media_sequence,
                    number=media_sequence,
                    duration=float(line.split(":")[1].split(",")[0]),
                    url=lines[i+1].strip()
                    )
            manifest.add_segment(segment)
            media_sequence += 1
