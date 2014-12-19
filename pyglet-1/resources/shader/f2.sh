uniform sampler2D tex0;
uniform vec2 pixel;

void main() {
        vec4 sum = vec4(0.0);

        float blur = 5.0;

        // retrieve the texture coordinate
        vec2 c = gl_TexCoord[0].xy;

        vec4 original = texture2D(tex0, c).rgba;

        float hstep = 1.0;
        float vstep = 0.0;

        sum += texture2D(tex0, vec2(c.x - 4.0*blur*hstep, c.y - 4.0*blur*vstep))* 0.0162162162;
        sum += texture2D(tex0, vec2(c.x - 3.0*blur*hstep, c.y - 3.0*blur*vstep))* 0.0540540541;
        sum += texture2D(tex0, vec2(c.x - 2.0*blur*hstep, c.y - 2.0*blur*vstep))* 0.1216216216;
        sum += texture2D(tex0, vec2(c.x - 1.0*blur*hstep, c.y - 1.0*blur*vstep))* 0.1945945946;

        sum += texture2D(tex0, vec2(c.x, c.y)) * 0.2270270270;

        sum += texture2D(tex0, vec2(c.x - 1.0*blur*hstep, c.y - 1.0*blur*vstep))* 0.1945945946;
        sum += texture2D(tex0, vec2(c.x - 2.0*blur*hstep, c.y - 2.0*blur*vstep))* 0.1216216216;
        sum += texture2D(tex0, vec2(c.x - 3.0*blur*hstep, c.y - 3.0*blur*vstep))* 0.0540540541;
        sum += texture2D(tex0, vec2(c.x - 4.0*blur*hstep, c.y - 4.0*blur*vstep))* 0.0162162162;

        gl_FragColor = original * vec4(sum.rgb, 1.0);

//       original.rgb = 1 - original.rgb;
//       gl_FragColor = vec4(original);
}