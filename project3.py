import os

import moderngl
import moderngl_window as mglw
from pyrr import Matrix44
import struct


class Window(mglw.WindowConfig):

    gl_version = (3, 3)
    title = "Project 3"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9

    resource_dir = os.path.normpath(os.path.join(__file__, '../data'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.obj = self.load_scene('teapot.obj')
        self.prog = self.load_program(
            vertex_shader="../shaders/prj3.vert",
            fragment_shader="../shaders/flat.frag"
        )
        self.mvp = self.prog["Mvp"]
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)
        self.up = (0, 0, 1)
        self.target = (0, 0, 5)
        self.camera_pos = (0, -30, 5)

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

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


if __name__ == '__main__':
    Window.run()
