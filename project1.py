import moderngl_window as mglw


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (640, 360)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colors = [(0.8, 0.2, 0.0), (0.5, 0.0, 0.5), (0.0, 0.5, 0.5)]
        self.time_to_change = 3

    def render(self, time, frame_time):
        t = (time % self.time_to_change) / self.time_to_change
        color_idx = int((time // self.time_to_change) % len(self.colors))
        current_color = self.colors[color_idx]
        self.ctx.clear(
            t * current_color[0], t * current_color[1], t * current_color[2]
        )

if __name__ == '__main__':
    Window.run()
