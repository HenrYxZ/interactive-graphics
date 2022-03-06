from math import radians, sin, cos
from pathlib import Path
from pyrr import Matrix44
import struct

import moderngl
import moderngl_window as mglw


# Local modules
from constants import *


class OrbitCameraWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Orbit Camera Window"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    resource_dir = Path(__file__).parent
    currently_pressed = 0
    sensitivity = 0.1
    angles_delta = 10
    zoom_speed = 0.1
    theta = -90
    phi = 90
    zoom = 30
    target = (0, 0, 5)
    up = (0, 0, 1)
    fov = 45.0
    far = 1000.0
    near = 0.1

    def __init__(self, progam_path, **kwargs):
        super().__init__(**kwargs)
        self.obj = self.load_scene('data/teapot.obj')
        self.prog = self.load_program(progam_path)
        self.proj = self.prog['proj']
        self.mv = self.prog['mv']
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
            delta_theta = -dx * self.sensitivity * self.angles_delta
            self.theta += delta_theta
            delta_phi = -dy * self.sensitivity * self.angles_delta
            self.phi += delta_phi
        elif self.currently_pressed == RIGHT_BUTTON:
            # Adjust zoom
            self.zoom += self.zoom_speed * dy

    def update_mvp(self):
        proj = Matrix44.perspective_projection(
            self.fov, self.aspect_ratio, self.near, self.far
        )
        theta_rads = radians(self.theta)
        phi_rads = radians(self.phi)
        eye_x = self.zoom * cos(theta_rads) * sin(phi_rads)
        eye_y = self.zoom * sin(theta_rads) * sin(phi_rads)
        eye_z = self.zoom * cos(phi_rads) + 5
        eye = (eye_x, eye_y, eye_z)
        lookat = Matrix44.look_at(eye, self.target, self.up)

        self.mv.write(lookat.astype('f4'))
        self.proj.write(proj.astype('f4'))

    def render(self, time, frame_time):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.update_mvp()
        self.vao.render(moderngl.TRIANGLES)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)
