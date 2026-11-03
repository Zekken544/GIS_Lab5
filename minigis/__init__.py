from dataclasses import dataclass
from pathlib import Path

from .features import Feature, Point, Polygon, Polyline
from .read_shapefile import read_shapes


@dataclass
class Layer:
    path: Path
    features: list[Feature]


def load_layer(path):
    kind, _, records = read_shapes(path)
    feature = {1: Point, 3: Polyline, 5: Polygon}[kind]
    return Layer(path, [feature(parts) for _, _, _, parts in records if parts])
