import os
from pyrr import Matrix44
import struct

import moderngl
import moderngl_window as mglw


class LoadingOBJ(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL Example"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    resource_dir = os.path.normpath(os.path.join(__file__, '../data'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.obj = self.load_scene('teapot.obj')

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec3 in_position;
                uniform float scale;
                void main() {
                    vec3 pos = scale * in_position;
                    gl_Position = vec4(pos, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330
                out vec4 f_color;
                void main() {
                    f_color = vec4(1.0, 1.0, 1.0, 1.0);
                }
            ''',
        )
        # self.mvp = self.prog['Mvp']
        self.scale = self.prog['scale']
        # Create a vao from the first root node (attribs are auto mapped)
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

    def render(self, time, frame_time):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        proj = Matrix44.perspective_projection(
            45.0, self.aspect_ratio, 0.1, 1000.0
        )
        eye = (0.0, 0.0, -3.0)
        target = (0.0, 0.0, 0.0)
        up = (0.0, 1.0, 0.0)
        lookat = Matrix44.look_at(eye, target, up)

        # self.mvp.write((proj * lookat).astype('f4'))
        self.scale.write(struct.pack('f', 0.05))
        self.vao.render(moderngl.POINTS)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


if __name__ == '__main__':
    LoadingOBJ.run()
