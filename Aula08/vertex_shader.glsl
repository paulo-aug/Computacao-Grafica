#version 120

varying vec3 Normal;
varying vec3 Position;

void main()
{
    Position = vec3(gl_ModelViewMatrix * gl_Vertex);
    Normal = normalize(gl_NormalMatrix * gl_Normal);

    gl_Position = ftransform();
}