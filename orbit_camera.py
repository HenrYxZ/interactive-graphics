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
    theta = -58
    phi = 109
    zoom = 45
    target = (0, 0, 5)
    up = (0, 0, 1)
    fov = 45.0
    far = 1000.0
    near = 0.1
    uses_eye = False
    uses_light = False
    l_theta = -37
    l_phi = 123
    l_r = 20
    light_pos = (
        l_r * sin(radians(l_theta)) * cos(radians(l_phi)),
        l_r * sin(radians(l_theta)) * sin(radians(l_phi)),
        l_r * cos(radians(l_phi))
    )
    move_light = False

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
            delta_theta = dy * self.sensitivity * self.angles_delta
            delta_phi = -dx * self.sensitivity * self.angles_delta

            if self.move_light:
                self.l_theta += delta_theta * 0.5
                self.l_phi += delta_phi * 0.5
                self.l_theta = min(max(-90, self.l_theta), 90)
            else:
                # Adjust camera angle
                self.theta += delta_theta
                self.phi += delta_phi
        elif self.currently_pressed == RIGHT_BUTTON:
            # Adjust zoom
            self.zoom += self.zoom_speed * dy

    def key_event(self, key, action, modifiers):
        # Key presses
        keys = self.wnd.keys
        if action == keys.ACTION_PRESS:
            if modifiers.ctrl:
                self.move_light = True

        # Key releases
        elif action == keys.ACTION_RELEASE:
            if not modifiers.ctrl:
                self.move_light = False

    def update_mvp(self):
        proj = Matrix44.perspective_projection(
            self.fov, self.aspect_ratio, self.near, self.far
        )
        theta_rads = radians(self.theta)
        phi_rads = radians(self.phi)
        eye_x = self.zoom * cos(phi_rads) * sin(theta_rads)
        eye_y = self.zoom * sin(phi_rads) * sin(theta_rads)
        eye_z = self.zoom * cos(theta_rads) + 5
        eye = (eye_x, eye_y, eye_z)
        lookat = Matrix44.look_at(eye, self.target, self.up)

        if self.uses_eye:
            self.prog['eye'].value = eye
        self.mv.write(lookat.astype('f4'))
        self.proj.write(proj.astype('f4'))

    def update_light(self):
        theta = radians(self.l_theta)
        phi = radians(self.l_phi)
        self.light_pos = (
            self.l_r * sin(theta) * cos(phi),
            self.l_r * sin(theta) * sin(phi),
            self.l_r * cos(theta)
        )
        if self.uses_light:
            self.prog['light_pos'].value = self.light_pos

    def render(self, time, frame_time):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.update_mvp()
        self.update_light()
        self.vao.render(moderngl.TRIANGLES)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)
