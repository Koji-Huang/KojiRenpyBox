"""renpy

init python:
"""


renpy.register_shader("dust",
    variables = """
        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        uniform float u_lod_bias;
        varying vec2 v_uv;
        uniform float u_anima_time;
        uniform float u_time;
    """,
    vertex_50="""
        v_uv = a_tex_coord;
    """,
    fragment_functions="""
        float get_time(vec2 pos, float randint, float time){

            randint = fract(sin(randint) / randint * 1024);
            pos *= 1000;
            float rand = fract(fract(fract(log(pos.x / randint * 114.514 + pos.y / randint * 191.981) * 13 + 11) / randint + sin(pos.x*11.45) + cos(pos.y*19.1981)) * 1314.1024);

            return clamp(1.0 + rand - time*2, 0.0, 1.0);
        }

    """,
    fragment_300="""
        gl_FragColor = texture2D(tex0, v_uv, u_lod_bias) * get_time(v_uv, 114514, u_anima_time);
    """,
)


class DustLayer(renpy.Displayable):
    def __init__(self, obj, speed=1.0, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.model = Model()

        self.tex = renpy.displayable(obj)

        self.model.texture(self.tex)

        self.model.shader("dust")

        self.speed = speed

    def render(self, w, h, st, at):
        # 动画时间轴
        # anima = _warper.ease_quint(st/2%1)
        anima = st*self.speed%1

        # size = renpy.render(self.tex, w, h, st, at).get_size()
        size = w, h

        self.model.uniform("u_anima_time", anima)

        rv = renpy.Render(w, h)

        renpy.redraw(self, 0)
        renpy.redraw(self.model, 0)

        rend = renpy.render(self.model, *size, st, at)
        self.model.place(rv, 0, 0, *size, rend)

        return rv

    def event(self, ev, x, y, st):
        return self.model.event(ev, x, y, st)

