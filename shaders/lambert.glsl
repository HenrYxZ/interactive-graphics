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
    // mat3 m_normal = transpose(inverse(mat3(mv)));
    // v_norm = m_normal * in_normal;
    v_vert = in_position;
    v_norm = in_normal;
}


#elif defined FRAGMENT_SHADER

in vec3 v_vert;
in vec3 v_norm;
vec3 light = vec3(20.0, 0.0, 7.0);

out vec4 f_color;

void main() {
    vec3 l = normalize(light - v_vert);
    f_color = vec4(dot(l, v_norm) * vec3(1.0, 1.0, 1.0), 1.0);
}

#endif