#version 330

#if defined VERTEX_SHADER

uniform mat4 mv;
uniform mat4 proj;

in vec3 in_position;

void main()
{
    gl_Position = proj * mv * vec4(in_position, 1.0);
}


#elif defined FRAGMENT_SHADER

out vec4 f_color;

void main() {
    f_color = vec4(1.0, 0.0, 0.0, 1.0);
}

#endif