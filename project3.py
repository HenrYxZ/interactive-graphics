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


class Window(mglw.WindowConfig):

    gl_version = (3, 3)
    title = "Project 3"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9

    resource_dir = Path(__file__).parent

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
        super().__init__(**kwargs)
        self.obj = self.load_scene('data/teapot.obj')
        self.render_modes = self.create_render_modes()
        self.prog = self.render_modes[NORMAL_SHADER]
        self.mvp = self.prog["Mvp"]
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)
        self.up = (0, 0, 1)
        self.target = (0, 0, 5)
        self.camera_pos = (0, -30, 5)

    def set_render_mode(self, mode):
        self.prog = self.render_modes[mode]
        self.mvp = self.prog["Mvp"]
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

    def render(self, time, frame_time):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.vao.render()
        fov = 45.0
        far = 1000.0
        near = 0.1
        proj = Matrix44.perspective_projection(
            fov, self.aspect_ratio, near, far
        )
        lookat = Matrix44.look_at(self.camera_pos, self.target, self.up)

        self.mvp.write((proj * lookat).astype('f4'))
        self.vao.render(moderngl.TRIANGLES)

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
