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

uniform vec3 eye;
uniform vec3 light_pos;
uniform float alpha;

in vec3 v_vert;
in vec3 v_norm;

out vec4 f_color;

void main() {
    vec3 view = normalize(eye - v_vert);
    vec3 l = normalize(light_pos - v_vert);
    vec3 h = normalize(l + view);
    float specular_term = pow(dot(h, v_norm), alpha);
    f_color = vec4(specular_term * vec3(1.0, 1.0, 1.0), 1.0);
}

#endif