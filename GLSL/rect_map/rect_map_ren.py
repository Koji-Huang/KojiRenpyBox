"""renpy

init python:
"""

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
    def __init__(self, number = (16*5, 9*5), color = ("#666", "#000")):
        super().__init__()
        self.model = Model()
        self.model.shader("rect_map")
        self.model.uniform("u_number", number)
        self.model.uniform("u_color_A", Color(color[0]).rgba)
        self.model.uniform("u_color_B", Color(color[1]).rgba)
    
    def render(self, w, h, st, at):
        return self.model.render(w, h, st, at)