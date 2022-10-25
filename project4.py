import moderngl


from constants import SPECULAR_ALPHA
from orbit_camera import OrbitCameraWindow


class Window(OrbitCameraWindow):
    def __init__(self, **kwargs):
        scene_path = 'data/teapot.obj'
        program_path = 'shaders/textured.glsl'
        super(Window, self).__init__(scene_path, program_path, **kwargs)
        self.specular_tex = self.load_texture_2d('data/brick-specular.png')
        self.specular_tex.build_mipmaps()
        # Activate texture
        self.obj.root_nodes[0].mesh.material.mat_texture.texture.use()
        self.set_light_col()
        self.set_ambient_col()
        self.set_specular_alpha()
        self.uses_eye = True
        self.uses_light = True
        self.prog['texture1'].value = 1

    # Set Shader Attributes
    def set_light_col(self):
        self.prog['light_col'].value = (1, 1, 1)

    def set_ambient_col(self):
        self.prog['ambient_col'].value = (1, 1, 1)

    def set_specular_alpha(self):
        self.prog['alpha'] = SPECULAR_ALPHA

    def render(self, time, frame_time):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.update_mvp()
        if self.uses_light:
            self.update_light()
        self.specular_tex.use(location=1)
        self.vao.render(moderngl.TRIANGLES)


if __name__ == '__main__':
    Window.run()
