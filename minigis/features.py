from dataclasses import dataclass
from math import dist


@dataclass
class Feature:
    parts: list

    def vis(self, canvas, transform):
        raise NotImplementedError


class Point(Feature):
    def vis(self, canvas, transform):
        for part in self.parts:
            x, y = transform(*part[0])
            canvas.create_oval(x-4, y-4, x+4, y+4, fill="#b93b28", outline="")


class Polyline(Feature):
    def length(self):
        return sum(dist(a, b) for part in self.parts for a, b in zip(part, part[1:]))

    def draw_parts(self, canvas, transform, color):
        for part in self.parts:
            pixels = [value for point in part for value in transform(*point)]
            canvas.create_line(*pixels, fill=color, width=2)

    def vis(self, canvas, transform):
        self.draw_parts(canvas, transform, "#245ba4")


class Polygon(Polyline):
    def vis(self, canvas, transform):
        self.draw_parts(canvas, transform, "#16774c")
