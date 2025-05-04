"""renpy

init python:
"""


renpy.register_shader("particle",
    variables = """

        uniform sampler2D tex0;
        uniform sampler2D tex1;

        attribute vec2 a_tex_coord;
        uniform float u_lod_bias;
        varying vec2 v_uv;
        uniform float u_time;

        uniform float u_percent;
        uniform float u_anima_during;
        uniform float u_anima_time;
        uniform float u_randint;
        uniform vec4 u_col;
        uniform vec2 u_center;
        
        uniform float u_has_second_tex;
    """,

    vertex_50="""
        v_uv = a_tex_coord;
    """,

    fragment_functions="""

        vec2 get_origin_pos(vec2 pos, vec2 v, vec2 offset, float time){ return pos - v * time + offset;}

        vec2 offset_func(vec2 pos, float randint, float time){
            randint = (sin(randint + pos.x * 10 + time * 3.0) + cos(randint + pos.y * 10 + time * 3.0)) * 1 + 0.8;
            return vec2(sin(pos.x + randint), cos(pos.y + randint)) / 40;
        }

        float convert_percent(float val, float percent){ return (val>percent)?(val-percent) / (1.0 - percent):0.0;}

        vec4 render_per_time(float time, float percent, vec2 center, float randint, float lod_bias, vec2 uv, float enable_color_tex, sampler2D mask_tex, sampler2D color_tex){

            percent = percent + (1.0 - percent) * abs(time - 0.5) * 2;
        
            vec2 new_uv = get_origin_pos(uv, (uv - center) / 1.2, offset_func(uv, randint, time), time);
            
            float col = texture2D(mask_tex, new_uv, lod_bias).r;

            float weight = convert_percent(col, percent);

            if(weight != 0.0) 
                if(enable_color_tex < 0.5) return vec4(weight, weight, weight, 1.0);
                else return texture2D(color_tex, new_uv, lod_bias) * weight;

            return vec4(0.0, 0.0, 0.0, 0.0);

        }
    """,

    fragment_300="""
        float percent = u_percent + (1.0 - u_percent) * abs(u_anima_during - 0.5) * 2;
    
        if(u_anima_time > 0.0){
            float time = fract(u_anima_time);
            float randint = u_randint + ceil(u_anima_time);
            gl_FragColor = render_per_time(time, percent, u_center, randint, u_lod_bias, v_uv, u_has_second_tex, tex0, tex1);
            }

        if(u_anima_time > 0.3){
            float time = fract(u_anima_time - 0.3);
            float randint = u_randint + ceil(u_anima_time - 0.3);
            gl_FragColor += render_per_time(time, percent, u_center, randint, u_lod_bias, v_uv, u_has_second_tex, tex0, tex1);
            }

        if(u_anima_time > 0.6){
            float time = fract(u_anima_time - 0.6);
            float randint = u_randint + ceil(u_anima_time - 0.6);
            gl_FragColor += render_per_time(time, percent, u_center, randint, u_lod_bias, v_uv, u_has_second_tex, tex0, tex1);
            }
        
        if(u_has_second_tex < 0.5)
            gl_FragColor *= u_col;
    """,
)


class ParticleLayer(renpy.Displayable):
    def __init__(self, mask, obj=None, percent=0.7, randint=116, center=(0.5, 0.5), speed=1.0, color=(1.0, 1.0, 1.0, 0.0), *args, **kwargs):
        """
        @param mask: 粒子分布的权重图像
        @param obj: 粒子的纹理图像, 不存在时默认使用 color, 存在时禁用 color
        @param percent: 当一个点的权重高于 percent 时才会被绘制
        @param randint: 随机数, 多图层叠加就用得到了
        @param center: 粒子发射位置的中心
        @param speed: 动画发生的速度
        @param color: 在没有纹理图像时粒子绘制的颜色
        """

        super().__init__(*args, **kwargs)
        self.model = Model()

        self.mask = renpy.displayable(mask)
        self.tex = None

        self.model.texture(self.mask)

        self.model.shader("particle")

        self.model.uniform("u_percent", percent)
        self.model.uniform("u_randint", randint)
        self.model.uniform("u_center", center)
        self.model.uniform("u_anima_during", 0.5)
        self.model.uniform("u_col", color)
        self.model.uniform("u_has_second_tex", False)

        if obj is not None:
            self.tex = renpy.displayable(obj)
            self.model.texture(self.tex)
            self.model.uniform("u_has_second_tex", True)
        else:
            self.model.texture(Null())
            

        self.speed = speed

    def render(self, w, h, st, at):
        # 动画时间轴
        anima = st*self.speed

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

