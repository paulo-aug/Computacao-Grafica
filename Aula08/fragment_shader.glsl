#version 120

uniform float tempo;
uniform float shininess;

varying vec3 Normal;
varying vec3 Position;

void main()
{
    vec3 luzPos = vec3(2.0, 2.0, 2.0);

    vec3 normal = normalize(Normal);
    vec3 lightDir = normalize(luzPos - Position);

    // Difusa
    float diff = max(dot(normal, lightDir), 0.0);

    vec3 corOriginal = vec3(0.0, 0.0, 1.0);

    // Exercício 1
    float alerta = (sin(tempo * 2.0) + 1.0) / 2.0;

    vec3 corDifusa = mix(corOriginal, vec3(1.0, 0.0, 0.0), alerta);

    // Especular
    vec3 viewDir = normalize(-Position);
    vec3 reflectDir = reflect(-lightDir, normal);

    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);

    vec3 cor = corDifusa * diff + vec3(spec);

    gl_FragColor = vec4(cor, 1.0);
}