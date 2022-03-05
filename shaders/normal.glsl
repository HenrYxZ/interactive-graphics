#version 330

#if defined VERTEX_SHADER

uniform mat4 Mvp;

in vec3 in_position;
in vec3 in_normal;

out vec3 v_norm;


void main() {
    gl_Position = Mvp * vec4(in_position, 1.0);
    v_norm = in_normal;
}

#elif defined FRAGMENT_SHADER

in vec3 v_norm;

out vec4 f_color;

void main() {
    f_color =clamp(vec4(normalize(v_norm), 1.0), 0.0, 1.0);
}

#endif
