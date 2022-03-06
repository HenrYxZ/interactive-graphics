import moderngl
import moderngl_window as mglw
from pathlib import Path
from pyrr import Matrix44
import struct


from orbit_camera import OrbitCameraWindow

FLAT_SHADER = 0
NORMAL_SHADER = 1
LAMBERT_SHADER = 2
SPECULAR_SHADER = 3
BLINN_SHADER = 4


class Window(OrbitCameraWindow):

    title = "Project 3"

    def create_render_modes(self):
        modes = {
            FLAT_SHADER: self.load_program("shaders/flat.glsl"),
            NORMAL_SHADER: self.load_program("shaders/normal.glsl"),
            LAMBERT_SHADER: self.load_program("shaders/lambert.glsl"),
            SPECULAR_SHADER: self.load_program("shaders/specular.glsl"),
            BLINN_SHADER: self.load_program("shaders/blinn.glsl")
        }
        return modes

    def __init__(self, **kwargs):
        super().__init__("shaders/normal.glsl", **kwargs)
        self.render_modes = self.create_render_modes()

    def set_render_mode(self, mode):
        self.prog = self.render_modes[mode]
        self.proj = self.prog['proj']
        self.mv = self.prog['mv']
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

    def key_event(self, key, action, modifiers):
        # Key presses
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.NUMBER_1:
                self.set_render_mode(FLAT_SHADER)
            elif key == self.wnd.keys.NUMBER_2:
                self.set_render_mode(NORMAL_SHADER)
            elif key == self.wnd.keys.NUMBER_3:
                self.set_render_mode(LAMBERT_SHADER)
            elif key == self.wnd.keys.NUMBER_4:
                self.set_render_mode(SPECULAR_SHADER)
            elif key == self.wnd.keys.NUMBER_5:
                self.set_render_mode(BLINN_SHADER)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


if __name__ == '__main__':
    Window.run()
