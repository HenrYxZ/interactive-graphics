#version 330

#if defined VERTEX_SHADER

uniform mat4 proj;
uniform mat4 mv;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec3 v_vert;
out vec3 v_norm;
out vec2 v_tex;


void main() {
    gl_Position = proj * mv * vec4(in_position, 1.0);
    v_vert = in_position;
    v_norm = in_normal;
    v_tex = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

uniform vec3 light_col;
uniform vec3 light_pos;
uniform vec3 ambient_col;
uniform sampler2D texture0;
uniform vec3 eye;
uniform float alpha;

in vec3 v_norm;
in vec3 v_vert;
in vec2 v_tex;

vec3 Kd = vec3(0.50980395, 0.0, 0.0);
vec3 Ka = vec3(0.50980395, 0.0, 0.0);
vec3 Ks = vec3(0.80099994, 0.80099994, 0.80099994);

out vec4 f_color;

void main() {
    vec3 diff_col = texture(texture0, v_tex).rgb;
    vec3 l = normalize(light_pos - v_vert);
    vec3 diffuse = clamp(dot(l, v_norm) * diff_col, 0.0, 1.0);
    vec3 ambient = diff_col * ambient_col;
    vec3 view = normalize(eye - v_vert);
    vec3 h = normalize(l + view);
    float specular = clamp(dot(h, v_norm), 0.0, 1.0);
    vec3 color = (
        light_col * (Kd * diffuse + Ks * pow(specular, alpha)) +
        ambient_col * Ka * ambient
    );
    f_color = vec4(clamp(color, 0.0, 1.0), 1.0);
}

#endif