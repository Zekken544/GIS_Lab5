import struct

TYPES = {1: "Point", 3: "Polyline", 5: "Polygon"}


def header(data):
    code, = struct.unpack_from(">i", data)
    words, = struct.unpack_from(">i", data, 24)
    version, kind, *bounds = struct.unpack_from("<2i8d", data, 28)
    if code != 9994 or version != 1000 or words * 2 != len(data) or kind not in TYPES:
        raise ValueError("Invalid or unsupported shapefile header")
    return kind, tuple(bounds[:4])


def read_shapes(path):
    shp = path.read_bytes()
    shx = path.with_suffix(".shx").read_bytes()
    kind, bounds = header(shp)
    if header(shx) != (kind, bounds) or (len(shx) - 100) % 8:
        raise ValueError("Invalid shapefile index")
    records = []
    expected = 100
    for words, length in struct.iter_unpack(">2i", shx[100:]):
        offset = words * 2
        end = offset + 8 + length * 2
        if offset != expected or length < 2 or end > len(shp):
            raise ValueError("Invalid record offset or length")
        expected = end
        number, stored_length = struct.unpack_from(">2i", shp, offset)
        if stored_length != length:
            raise ValueError("Index and record lengths differ")
        body = shp[offset + 8:end]
        shape, = struct.unpack_from("<i", body)
        if shape == 0:
            if len(body) != 4:
                raise ValueError("Invalid null record")
            parts = []
        elif shape != kind:
            raise ValueError("Record type differs from file type")
        elif shape == 1:
            _, x, y = struct.unpack("<i2d", body)
            parts = [[(x, y)]]
        else:
            count, total = struct.unpack_from("<2i", body, 36)
            start = 44 + count * 4
            if not 1 <= count <= total or len(body) != start + total * 16:
                raise ValueError("Invalid part or vertex count")
            indices = [i for i, in struct.iter_unpack("<i", body[44:start])]
            ends = indices[1:] + [total]
            minimum = 2 if shape == 3 else 4
            if indices[0] != 0 or any(b - a < minimum for a, b in zip(indices, ends)):
                raise ValueError("Invalid part indices")
            vertices = list(struct.iter_unpack("<2d", body[start:]))
            parts = [vertices[a:b] for a, b in zip(indices, ends)]
            if shape == 5 and any(p[0] != p[-1] for p in parts):
                raise ValueError("Unclosed polygon ring")
        records.append((number, offset, length * 2, parts))
    if expected != len(shp):
        raise ValueError("Index does not cover the main file")
    return kind, bounds, records



