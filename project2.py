import os
import numpy as np
from pyrr import Matrix44
import struct

import moderngl
import moderngl_window as mglw


# Local modules
from constants import *


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL Example"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    resource_dir = os.path.normpath(os.path.join(__file__, '../data'))
    cam_target = np.array([0, 0, 0])
    currently_pressed = 0
    sensitivity = 0.1
    angles_delta = 10
    zoom_speed = 0.1
    theta = 90
    phi = 90
    zoom = 3
    up = (0, 0, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.obj = self.load_scene('teapot.obj')

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec3 in_position;
                uniform float scale;
                uniform mat4 Mvp;
                void main() {
                    vec3 pos = scale * in_position;
                    gl_Position = Mvp * vec4(pos, 1.0);
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
        self.mvp = self.prog['Mvp']
        self.scale = self.prog['scale']
        # Create a vao from the first root node (attribs are auto mapped)
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

    def mouse_press_event(self, x, y, button):
        if 0 <= x <= self.window_size[0] and 0 <= y <= self.window_size[1]:
            self.currently_pressed = button

    def mouse_release_event(self, x, y, _):
        if 0 <= x <= self.window_size[0] and 0 <= y <= self.window_size[1]:
            self.currently_pressed = 0

    def mouse_drag_event(self, _, __, dx, dy):
        if self.currently_pressed == LEFT_BUTTON:
            # Adjust camera angle
            delta_theta = dx * self.sensitivity * self.angles_delta
            self.theta += delta_theta
            delta_phi = dy * self.sensitivity * self.angles_delta
            self.phi += delta_phi
        elif self.currently_pressed == RIGHT_BUTTON:
            # Adjust zoom
            self.zoom += self.zoom_speed * dy

    def render(self, time, frame_time):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        fov = 45.0
        far = 1000.0
        near = 0.1
        proj = Matrix44.perspective_projection(
            fov, self.aspect_ratio, near, far
        )
        theta_rads = np.radians(self.theta)
        phi_rads = np.radians(self.phi)
        eye_x = self.zoom * np.cos(theta_rads) * np.sin(phi_rads)
        eye_y = self.zoom * np.sin(theta_rads) * np.sin(phi_rads)
        eye_z = self.zoom * np.cos(phi_rads)
        eye = (eye_x, eye_y, eye_z)
        target = (0.0, 0.0, 0.0)
        lookat = Matrix44.look_at(eye, target, self.up)

        self.mvp.write((proj * lookat).astype('f4'))
        self.scale.write(struct.pack('f', 0.05))
        self.vao.render(moderngl.POINTS)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


if __name__ == '__main__':
    Window.run()
