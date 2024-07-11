import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .model import Schelling


class Visualizer:
    COLOR_TYPE_0 = (93, 147, 183)
    COLOR_TYPE_1 = (14, 61, 144)
    COLOR_EMPTY = (255, 255, 255)

    def __init__(self, schelling: Schelling) -> None:
        self.schelling = schelling
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.axes.xaxis.set_ticks([])
        self.ax.axes.yaxis.set_ticks([])
        self.fig.tight_layout()
        self.im = self.ax.imshow(self.generate_color_map())

    def generate_color_map(self) -> np.ndarray:
        type_map = self.schelling.generate_type_map()

        def get_color(type_):
            if type_ == 0:
                return self.COLOR_TYPE_0
            elif type_ == 1:
                return self.COLOR_TYPE_1
            else:
                return self.COLOR_EMPTY

        return np.array([[get_color(type_) for type_ in row] for row in type_map])

    def update(self, _, updates_per_frame) -> list:
        for _ in range(updates_per_frame):
            self.schelling.update()
        self.im.set_data(self.generate_color_map())
        return [self.im]

    def animate(self, updates_per_frame=100, interval=200) -> None:
        anim = FuncAnimation(
            self.fig,
            self.update,
            interval=interval,
            fargs=(updates_per_frame,),
        )
        plt.show()
