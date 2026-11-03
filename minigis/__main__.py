import argparse
from pathlib import Path

from . import load_layer
from .features import Polyline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-gui", action="store_true")
    args = parser.parse_args()
    paths = sorted((Path(__file__).resolve().parent.parent / "data").glob("*.shp"))
    if args.no_gui:
        for path in paths:
            layer = load_layer(path)
            length = sum(feature.length() for feature in layer.features if isinstance(feature, Polyline))
            print(f"{path.name}: {len(layer.features)} feature(s), line/ring length={length:.3f}")
    else:
        from .app import run
        run(paths)


if __name__ == "__main__":
    main()
