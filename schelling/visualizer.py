import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation, PillowWriter
from .model import Schelling


class Visualizer:

    def __init__(self, schelling: Schelling) -> None:
        self.schelling = schelling

        if self.schelling.number_types <= 4:
            self.colors = {
                None: mcolors.to_rgb("#FFFFFF"),
                0: mcolors.to_rgb("#5d93b7"),
                1: mcolors.to_rgb("#325e88"),
                2: mcolors.to_rgb("#95aec2"),
                3: mcolors.to_rgb("#092d5c"),
            }
        else:
            self.colors = {None: mcolors.to_rgb("#FFFFFF")} | {
                type_: mcolors.to_rgb(color)
                for type_, color in enumerate(mcolors.TABLEAU_COLORS)
            }

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.axes.xaxis.set_ticks([])
        self.ax.axes.yaxis.set_ticks([])
        self.fig.tight_layout()
        self.im = self.ax.imshow(self.generate_color_map())

    def generate_color_map(self) -> np.ndarray:
        return np.array(
            [
                [self.colors[type_] for type_ in row]
                for row in self.schelling.generate_type_map()
            ]
        )

    def update(self, _, updates_per_frame) -> list:
        for _ in range(updates_per_frame):
            self.schelling.update()
        self.im.set_data(self.generate_color_map())
        return [self.im]

    def animate(self, updates_per_frame, frames=None, interval=200) -> FuncAnimation:
        return FuncAnimation(
            self.fig,
            self.update,
            frames=frames,
            fargs=(updates_per_frame,),
            interval=interval,
            cache_frame_data=False,
        )

    def plot(self, updates_per_frame, interval=None) -> None:
        anim = self.animate(updates_per_frame, interval=interval)
        plt.show()

    def save(self, filename, frames=100, updates_per_frame=100, fps=10) -> None:
        anim = self.animate(updates_per_frame, frames=frames)
        anim.save(filename + ".gif", writer=PillowWriter(fps=fps))
