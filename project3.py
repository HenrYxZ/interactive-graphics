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

DIFFUSE_COLOR = (0.8, 0, 0)
SPECULAR_ALPHA = 40


class Window(OrbitCameraWindow):

    title = "Project 3"
    current_mode = FLAT_SHADER

    def create_render_modes(self):
        modes = {
            FLAT_SHADER: self.load_program("shaders/flat.glsl"),
            NORMAL_SHADER: self.load_program("shaders/normal.glsl"),
            LAMBERT_SHADER: self.load_program("shaders/lambert.glsl"),
            SPECULAR_SHADER: self.load_program("shaders/specular.glsl"),
            BLINN_SHADER: self.load_program("shaders/blinn.glsl")
        }
        return modes

    # Set Shader Attributes
    def set_material_color(self):
        self.prog['diff_col'].value = DIFFUSE_COLOR

    def set_light_pos(self):
        self.prog['light_pos'].value = self.light_pos

    def set_light_col(self):
        self.prog['light_col'].value = (1, 1, 1)

    def set_ambient_col(self):
        self.prog['ambient_col'].value = (1, 1, 1)

    def set_light(self):
        self.set_light_pos()
        self.set_light_col()

    def set_specular_alpha(self):
        self.prog['alpha'] = SPECULAR_ALPHA

    # Set Shaders
    def set_flat_shader(self):
        self.set_material_color()

    def set_lambert_shader(self):
        self.set_material_color()
        self.set_light()
        self.set_ambient_col()
        self.uses_light = True

    def set_specular_shader(self):
        self.set_light_pos()
        self.set_specular_alpha()
        self.uses_eye = True
        self.uses_light = True

    def set_blinn_shader(self):
        self.set_material_color()
        self.set_light()
        self.set_ambient_col()
        self.set_specular_alpha()
        self.uses_eye = True
        self.uses_light = True

    def set_render_mode(self, mode):
        self.current_mode = mode
        self.prog = self.render_modes[mode]
        self.proj = self.prog['proj']
        self.mv = self.prog['mv']
        self.uses_eye = False
        self.uses_light = False

        set_functions = {
            FLAT_SHADER: self.set_flat_shader,
            NORMAL_SHADER: lambda: None,
            LAMBERT_SHADER: self.set_lambert_shader,
            SPECULAR_SHADER: self.set_specular_shader,
            BLINN_SHADER: self.set_blinn_shader
        }
        set_functions[self.current_mode]()

        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

    def __init__(self, **kwargs):
        super().__init__("shaders/flat.glsl", **kwargs)
        self.render_modes = self.create_render_modes()
        self.set_render_mode(self.current_mode)

    def key_event(self, key, action, modifiers):
        super(Window, self).key_event(key, action, modifiers)
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
