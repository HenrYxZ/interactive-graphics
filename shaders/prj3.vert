#version 330

uniform mat4 Mvp;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec3 v_vert;
out vec3 v_norm;
out vec2 v_tex;

void main() {
    gl_Position = Mvp * vec4(in_position, 1.0);
    v_vert = in_position;
    v_norm = in_normal;
    v_tex = in_texcoord_0;
}