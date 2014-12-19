uniform sampler2D tex0;
uniform vec2 pixel;
varying vec3 normal, lightDir0, lightDir1, eyeVec;

void main() {
        // retrieve the texture coordinate
        vec2 c = gl_TexCoord[0].xy;
        vec4 final_color =
        (gl_FrontLightModelProduct.sceneColor * gl_FrontMaterial.ambient) +
        (gl_LightSource[0].ambient * gl_FrontMaterial.ambient) +
        (gl_LightSource[1].ambient * gl_FrontMaterial.ambient);

        vec3 N = normalize(normal);
        vec3 L0 = normalize(lightDir0);
        vec3 L1 = normalize(lightDir1);

        float lambertTerm0 = dot(N,L0);
        float lambertTerm1 = dot(N,L1);

        if(lambertTerm0 > 0.0)
        {
            final_color += gl_LightSource[0].diffuse *
                           gl_FrontMaterial.diffuse *
                           lambertTerm0;

            vec3 E = normalize(eyeVec);
            vec3 R = reflect(-L0, N);
            float specular = pow( max(dot(R, E), 0.0),
                             gl_FrontMaterial.shininess );
            final_color += gl_LightSource[0].specular *
                           gl_FrontMaterial.specular *
                           specular;
        }
        if(lambertTerm1 > 0.0)
        {
            final_color += gl_LightSource[1].diffuse *
                           gl_FrontMaterial.diffuse *
                           lambertTerm1;

            vec3 E = normalize(eyeVec);
            vec3 R = reflect(-L1, N);
            float specular = pow( max(dot(R, E), 0.0),
                             gl_FrontMaterial.shininess );
            final_color += gl_LightSource[1].specular *
                           gl_FrontMaterial.specular *
                           specular;
        }
        vec4 fog = vec4(0.5,0.5,0.5,0.2);

        vec4 original = texture2D(tex0, c).rgba;
        //original.rgb = 1 - original.rgb;
        gl_FragColor = original * final_color * 2;
}