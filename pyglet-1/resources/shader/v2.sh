void main() {
        // transform the vertex position
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        // pass through the texture coordinate
        gl_TexCoord[0] = gl_MultiTexCoord0;
}