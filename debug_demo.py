from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import traceback
from zipfile import ZipFile

from minigis import load_layer


def main():
    for label, example in [("SyntaxError", "if True print(1)"), ("Runtime error", "1 / 0")]:
        try:
            exec(compile(example, "<lab5 demo>", "exec"))
        except (SyntaxError, ZeroDivisionError) as error:
            print(label, "".join(traceback.format_exception_only(type(error), error)).strip())
    try:
        layer = load_layer(Path("missing.shp"))
        print(layer)
    except OSError as error:
        print(type(error).__name__, error)
    finally:
        print("File demo finished")
    print("Module search starts at:", sys.path[0])
    with TemporaryDirectory(dir=".") as folder:
        archive = Path(folder) / "demo.zip"
        with ZipFile(archive, "w") as file:
            file.writestr("demo.txt", "Mini-GIS")
        with ZipFile(archive) as file:
            print(file.namelist())


if __name__ == "__main__":
    main()
