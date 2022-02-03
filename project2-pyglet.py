import pyglet

from pyglet.gl import *
from pyglet.graphics import ShaderGroup
from pyglet.graphics.shader import Shader, ShaderProgram


# ------------------------------------------------------------------------------
# GLSL Shaders
# ------------------------------------------------------------------------------

vert_src = """
    #version 330 core
    
    in vec3 vertices;

    uniform WindowBlock
    {
        mat4 projection;
        mat4 view;
    } window;
    void main()
    {
        vec4 pos = window.view * vec4(vertices, 1.0);
        gl_Position = window.projection * pos;
    }
    """

frag_src = """
    #version 330 core
    
    void main()
    {
        gl_FragColor = vec4(0.8, 0.8, 0.8, 1.0);
    }
    """
# ------------------------------------------------------------------------------

WIDTH = 720
HEIGHT = 480

window = pyglet.window.Window(WIDTH, HEIGHT, caption="Project 2")
# window.projection = pyglet.window.Mat4.perspective_projection(
#     0, WIDTH, 0, HEIGHT, z_near=0.1, z_far=255
# )

vert_shader = Shader(vert_src, 'vertex')
frag_shader = Shader(frag_src, 'fragment')
shader_program = ShaderProgram(vert_shader, frag_shader)
shader_group = ShaderGroup(shader_program)

batch = pyglet.graphics.Batch()

teapot = pyglet.model.load("data/teapot.obj")
vertex_count = teapot.vertex_lists[0].count
batch.add(
    vertex_count, GL_POINTS, shader_group,
    ('vertices3f', teapot.vertex_lists[0])
)


@window.event
def on_draw():
    window.clear()
    batch.draw()


if __name__ == '__main__':
    pyglet.app.run()
