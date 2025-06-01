"""renpy

init python:
"""

pass

renpy.register_shader("test_shader", 
    variables = """
        uniform float u_time;
        varying float v_gradient_done;
        varying vec2 uv;
        attribute vec4 a_position;
        
    """ ,
    vertex_0="""
        gl_Position = a_position;
    """,
    vertex_300="""
        v_gradient_done = (sin(u_time)+1.0)*0.5;
        uv = vec2(gl_Position.x, gl_Position.y);
    """,
    fragment_functions="""
        vec4 draw_circle(vec4 img, vec2 uv, vec2 center, float len, float width){
            float l = sqrt((uv.x-center.x)*(uv.x-center.x) * (1920.0/1080.0) * (1920.0/1080.0) + (uv.y-center.y)*(uv.y-center.y) );
            // return vec4(l);
            if(len<l && l<=len+width)
                { return vec4(1.0, 1.0, 1.0, 1.0); }
            return img;
        }
    """,
    fragment_300="""
        vec4 bg = vec4(0.0, 0.0, 0.0, 0.0);
        gl_FragColor += draw_circle(bg, uv, vec2(0.0, 0.0), (sin(0.0+v_gradient_done*10.0)+1.1)*0.6, 0.005);
        gl_FragColor += draw_circle(bg, uv, vec2(0.0, 0.0), (sin(0.15+v_gradient_done*10.0)+1.1)*0.6, 0.004);
        gl_FragColor += draw_circle(bg, uv, vec2(0.0, 0.0), (sin(0.3+v_gradient_done*10.0)+1.1)*0.6, 0.003);
        gl_FragColor += draw_circle(bg, uv, vec2(0.0, 0.0), (sin(0.45+v_gradient_done*10.0)+1.1)*0.6, 0.002);
    """
    )


renpy.register_shader("fade_label",
    variables = """
        uniform vec4 u_left_top;
        uniform vec4 u_left_buttom;
        uniform vec4 u_right_top;
        uniform vec4 u_right_buttom; 
        attribute vec2 a_tex_coord;
        varying vec2 uv;
    """,
    vertex_300="""
        uv = vec2(a_tex_coord.x, a_tex_coord.y);
    """,
    fragment_300="""
        //gl_FragColor = mix(u_left_top, u_left_buttom, uv.y);
        gl_FragColor = mix(mix(u_left_top, u_left_buttom, uv.y), mix(u_right_top, u_right_buttom, uv.y), uv.x);
        gl_FragColor *= gl_FragColor[3];
    """
)

class FadeLabel(renpy.Displayable):
    def __init__(self, color = ("#fff", "#fff", "#0000", "0000")):
        super().__init__()
        self.model = Model()
        self.model.shader("fade_label")
        self.model.uniform("u_left_top", Color(color[0]).rgba)
        self.model.uniform("u_left_buttom", Color(color[1]).rgba)
        self.model.uniform("u_right_top", Color(color[2]).rgba)
        self.model.uniform("u_right_buttom", Color(color[3]).rgba)
        self.model.texture(Null())
    
    def render(self, w, h, st, at):
        return self.model.render(w, h, st, at)


renpy.register_shader("rect_map",
    variables = """
        attribute vec4 a_position;
        uniform vec2 u_number;
        uniform vec4 u_color_A;
        uniform vec4 u_color_B;
        varying vec2 uv;
    """,
    vertex_0="""
        gl_Position = a_position;
    """,
    vertex_300="""
        uv = vec2(gl_Position.x * .5 + .5, -gl_Position.y * .5 + .5);
    """,
    fragment_300="""
        vec2 tmp = vec2(fract(uv.x*u_number.x), fract(uv.y*u_number.y));
        if((tmp.x > 0.5) == (tmp.y > 0.5)) gl_FragColor = u_color_A;
        else gl_FragColor = u_color_B;
    """
)


class RectMap(renpy.Displayable):
    def __init__(self, number = (16*5, 9*5), color = ("#333", "#000")):
        super().__init__()
        self.model = Model()
        self.model.shader("rect_map")
        self.model.uniform("u_number", number)
        self.model.uniform("u_color_A", Color(color[0]).rgba)
        self.model.uniform("u_color_B", Color(color[1]).rgba)
    
    def render(self, w, h, st, at):
        return self.model.render(w, h, st, at)




