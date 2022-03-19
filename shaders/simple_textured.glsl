#version 330

#if defined VERTEX_SHADER

uniform mat4 proj;
uniform mat4 mv;

in vec3 in_position;
//in vec3 in_normal;
in vec2 in_texcoord_0;

//out vec3 v_vert;
//out vec3 v_norm;
out vec2 v_tex;


void main() {
    gl_Position = proj * mv * vec4(in_position, 1.0);
//    v_vert = in_position;
//    v_norm = in_normal;
    v_tex = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

//uniform vec3 light_col;
//uniform vec3 light_pos;
// uniform vec3 ambient_col;
uniform sampler2D texture0;
//uniform vec3 eye;

//in vec3 v_vert;
//in vec3 v_norm;
in vec2 v_tex;

out vec4 frag_color;

void main() {
//    vec3 l = normalize(light_pos - v_vert);
//    float coeff = clamp(dot(l, v_norm), 0, 1);
//    frag_color = vec4(coeff * light_col * texture(texture0, v_tex).rgb, 1.0);
    frag_color = texture(texture0, v_tex);
//    frag_color = vec4(1.0, 1.0, 1.0, 1.0);
}

#endif