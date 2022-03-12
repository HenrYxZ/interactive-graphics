#version 330

#if defined VERTEX_SHADER

uniform mat4 proj;
uniform mat4 mv;

in vec3 in_position;
in vec3 in_normal;

out vec3 v_vert;
out vec3 v_norm;


void main() {
    gl_Position = proj * mv * vec4(in_position, 1.0);
    v_vert = in_position;
    v_norm = in_normal;
}


#elif defined FRAGMENT_SHADER

uniform vec3 light_col;
uniform vec3 ambient_col;
uniform vec3 light_pos;
uniform vec3 diff_col;

in vec3 v_norm;
in vec3 v_vert;

const float Kd = 0.8;
const float Ka = 1 - Kd;

out vec4 f_color;

void main() {
    vec3 l = normalize(light_pos - v_vert);
    vec3 diffuse = clamp(dot(l, v_norm) * diff_col * light_col, 0.0, 1.0);
    vec3 ambient = diff_col * ambient_col;
    f_color = vec4(Kd * diffuse + Ka * ambient, 1.0);
}

#endif