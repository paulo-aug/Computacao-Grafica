#version 120

uniform mat4 model;

void main()
{
    gl_Position = gl_ModelViewProjectionMatrix * model * gl_Vertex;
}