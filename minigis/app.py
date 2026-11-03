from pathlib import Path
import struct
import tkinter as tk
from tkinter import filedialog, messagebox

from . import load_layer

WIDTH, HEIGHT = 800, 520


def run(paths):
    root = tk.Tk()
    root.title("Lab 5 - Mini-GIS")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, background="white")
    canvas.pack()
    status = tk.StringVar()
    tk.Label(root, textvariable=status).pack()
    layers = []
    zoom = 1.0
    shift = [0, 0]
    drag = [0, 0]

    def draw():
        canvas.delete("all")
        status.set(" | ".join(layer.path.stem for layer in layers) or "No layers")
        points = [point for layer in layers for feature in layer.features
                  for part in feature.parts for point in part]
        if not points:
            return
        xs, ys = zip(*points)
        xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
        scales = [pixels / span for pixels, span in
                  ((WIDTH-60, xmax-xmin), (HEIGHT-60, ymax-ymin)) if span]
        scale = zoom * min(scales, default=1)

        def transform(x, y):
            return (WIDTH/2 + shift[0] + (x-(xmin+xmax)/2)*scale,
                    HEIGHT/2 + shift[1] - (y-(ymin+ymax)/2)*scale)

        for layer in layers:
            for feature in layer.features:
                feature.vis(canvas, transform)

    def extent():
        nonlocal zoom
        zoom = 1.0
        shift[:] = [0, 0]
        draw()

    def change_zoom(factor):
        nonlocal zoom
        zoom = max(0.1, min(30, zoom * factor))
        draw()

    def add(paths):
        for path in paths:
            try:
                layer = load_layer(Path(path))
            except (OSError, ValueError, struct.error) as error:
                messagebox.showerror("Cannot load layer", f"{path}\n{error}")
                continue
            if all(old.path.resolve() != layer.path.resolve() for old in layers):
                layers.append(layer)
        extent()

    def import_folder():
        folder = filedialog.askdirectory()
        if folder:
            add(sorted(Path(folder).glob("*.shp")))

    def remove_layer():
        if not layers:
            return
        dialog = tk.Toplevel(root)
        dialog.title("Close layer")
        choices = tk.Listbox(dialog, exportselection=False)
        choices.pack(fill="both", expand=True)
        for layer in layers:
            choices.insert(tk.END, layer.path.name)

        def close_selected():
            selected = choices.curselection()
            if selected:
                layers.pop(selected[0])
                extent()
                dialog.destroy()

        tk.Button(dialog, text="Close selected", command=close_selected).pack()
        dialog.grab_set()

    def start_drag(event):
        drag[:] = [event.x, event.y]

    def pan(event):
        shift[0] += event.x - drag[0]
        shift[1] += event.y - drag[1]
        start_drag(event)
        draw()

    menu = tk.Menu(root)
    file_menu = tk.Menu(menu, tearoff=False)
    file_menu.add_command(label="Add shapefile", command=lambda: add(
        filedialog.askopenfilenames(filetypes=[("Shapefile", "*.shp")])))
    file_menu.add_command(label="Import folder", command=import_folder)
    menu.add_cascade(label="File", menu=file_menu)
    view = tk.Menu(menu, tearoff=False)
    view.add_command(label="Zoom in", command=lambda: change_zoom(1.25))
    view.add_command(label="Zoom out", command=lambda: change_zoom(0.8))
    view.add_command(label="Zoom to extent", command=extent)
    view.add_command(label="Close layer", command=remove_layer)
    menu.add_cascade(label="View", menu=view)
    root.config(menu=menu)
    canvas.bind("<ButtonPress-1>", start_drag)
    canvas.bind("<B1-Motion>", pan)
    add(paths)
    root.mainloop()
