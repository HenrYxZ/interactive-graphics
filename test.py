from math import radians, sin, cos
from pathlib import Path
from pyrr import Matrix44
import struct

import moderngl
import moderngl_window as mglw
from moderngl_window.scene.camera import KeyboardCamera


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Test Window"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    resource_dir = Path(__file__).parent

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scene = self.load_scene('data/teapot.obj')
        self.camera = KeyboardCamera(
            self.wnd.keys, aspect_ratio=self.wnd.aspect_ratio
        )
        self.camera_enabled = True
        self.camera.projection.update(near=0.1, far=100.0)
        self.camera.velocity = 7.0
        self.camera.mouse_sensitivity = 0.3

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            self.camera.key_input(key, action, modifiers)

        if action == keys.ACTION_PRESS:
            if key == keys.C:
                self.camera_enabled = not self.camera_enabled
                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.cursor = not self.camera_enabled
            if key == keys.SPACE:
                self.timer.toggle_pause()

    def mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx, -dy)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

    def render(self, time, _):
        self.ctx.enable_only(moderngl.DEPTH_TEST)

        translation = Matrix44.from_translation((0, 0, -10))
        rotation = Matrix44.from_eulers((0, 0, 0))
        model_matrix = translation * rotation
        camera_matrix = self.camera.matrix * model_matrix

        self.scene.draw(
            projection_matrix=self.camera.projection.matrix,
            camera_matrix=camera_matrix,
            time=time,
        )


if __name__ == '__main__':
    mglw.run_window_config(Window)
