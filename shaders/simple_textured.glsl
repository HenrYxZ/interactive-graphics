#version 330

#if defined VERTEX_SHADER

uniform mat4 proj;
uniform mat4 mv;

in vec3 in_position;
in vec2 in_texcoord_0;

out vec2 v_tex;


void main() {
    gl_Position = proj * mv * vec4(in_position, 1.0);
    v_tex = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

uniform sampler2D texture0;

in vec2 v_tex;

out vec4 frag_color;

void main() {
    frag_color = texture(texture0, v_tex);
}

#endif