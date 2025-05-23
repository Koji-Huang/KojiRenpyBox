"""renpy

init python:
"""


renpy.register_shader("rect_color",
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

class RectColor(renpy.Displayable):
    def __init__(self, *color):
        super().__init__()
        self.model = Model()
        self.model.shader("rect_color")

        if bool(color) is False:
            color = ("#fff", "#0000", "#fff", "0000")

        self.model.uniform("u_left_top", Color(color[0]).rgba)
        self.model.uniform("u_right_top", Color(color[1]).rgba)
        self.model.uniform("u_left_buttom", Color(color[2]).rgba)
        self.model.uniform("u_right_buttom", Color(color[3]).rgba)
        self.model.texture(Null())
    
    def render(self, w, h, st, at):
        return self.model.render(w, h, st, at)
        