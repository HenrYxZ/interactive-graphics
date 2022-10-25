from constants import SPECULAR_ALPHA
from orbit_camera import OrbitCameraWindow


class Window(OrbitCameraWindow):
    def __init__(self, **kwargs):
        scene_path = 'data/teapot.obj'
        program_path = 'shaders/textured.glsl'
        super(Window, self).__init__(scene_path, program_path, **kwargs)
        # Activate texture
        self.obj.root_nodes[0].mesh.material.mat_texture.texture.use()
        self.set_light_col()
        self.set_ambient_col()
        self.set_specular_alpha()
        self.uses_eye = True
        self.uses_light = True

    # Set Shader Attributes
    def set_light_col(self):
        self.prog['light_col'].value = (1, 1, 1)

    def set_ambient_col(self):
        self.prog['ambient_col'].value = (1, 1, 1)

    def set_specular_alpha(self):
        self.prog['alpha'] = SPECULAR_ALPHA


if __name__ == '__main__':
    Window.run()
