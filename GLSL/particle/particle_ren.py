'''

Copyright 2025.5.5 Koji-Huang(koji233@163.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''

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
        uniform vec2 u_speed;
        uniform vec2 u_range;
        uniform vec2 u_weight;
        
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

        vec4 render_per_time(float time, float percent, vec2 center, float randint, float lod_bias, vec2 uv, vec2 speed, vec2 weight, vec2 range, float enable_color_tex, sampler2D mask_tex, sampler2D color_tex){

            percent = percent + (1.0 - percent) * abs(time - 0.5) * 2;
        
            vec2 new_uv = get_origin_pos(uv, (uv - center) * weight.x, offset_func(uv, randint, time * speed.y) * weight.y, time * speed.x);

            if(new_uv.x < 0.0 || new_uv.x > 1.0 || new_uv.y < 0.0 || new_uv.y > 1.0) return vec4(0.0, 0.0, 0.0, 0.0);
            
            float col = texture2D(mask_tex, new_uv, lod_bias).r;

            col = (col - range.x) / (range.y - range.x);

            float result = convert_percent(col, percent);

            if(result != 0.0) 
                if(enable_color_tex < 0.5) return vec4(result, result, result, 1.0);
                else return texture2D(color_tex, new_uv, lod_bias) * result;

            return vec4(0.0, 0.0, 0.0, 0.0);

        }
    """,

    fragment_300="""
        float percent = u_percent + (1.0 - u_percent) * abs(u_anima_during - 0.5) * 2;
    
        if(u_anima_time > 0.0){
            float time = fract(u_anima_time);
            float randint = u_randint + ceil(u_anima_time);
            gl_FragColor = render_per_time(time, percent, u_center, randint, u_lod_bias, v_uv, u_speed, u_weight, u_range, u_has_second_tex, tex0, tex1);
            }

        if(u_anima_time > 0.3){
            float time = fract(u_anima_time - 0.3);
            float randint = u_randint + ceil(u_anima_time - 0.3) + 5;
            gl_FragColor += render_per_time(time, percent, u_center, randint, u_lod_bias, v_uv, u_speed, u_weight, u_range, u_has_second_tex, tex0, tex1);
            }

        if(u_anima_time > 0.6){
            float time = fract(u_anima_time - 0.6);
            float randint = u_randint + ceil(u_anima_time - 0.6) + 10;
            gl_FragColor += render_per_time(time, percent, u_center, randint, u_lod_bias, v_uv, u_speed, u_weight, u_range, u_has_second_tex, tex0, tex1);
            }
        
        if(u_has_second_tex < 0.5)
            gl_FragColor *= u_col;
    """,
)


class ParticleLayer(renpy.Displayable):
    def __init__(
            self, 
            mask, 
            obj=None, 
            percent=0.7,
            randint=116, 
            center=(0.5, 0.5), 
            mask_range=(0.0, 1.0), 
            vector_speed=(1.0, 1.0), 
            vector_weight=(1.0, 1.0), 
            color=(1.0, 0.9, 0.5, 0.0), 

            speed=0.3, 
            delay=0.0,

            *args, 
            **kwargs):

        """
        :param mask: 粒子分布权重纹理
        :param obj: 粒子着色纹理
        :param percent: 权重临界
        :param range: 权重的上下界
        :param randint: 随机数种子
        :param center: 粒子发射中心
        :param vector_speed: 向量的速度
        :param speed: 动画的速度
        :praram color: 没有着色纹理下粒子的颜色
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
        self.model.uniform("u_speed", vector_speed)
        self.model.uniform("u_weight", vector_weight)
        self.model.uniform("u_range", mask_range)

        if obj is not None:
            self.tex = renpy.displayable(obj)
            self.model.texture(self.tex)
            self.model.uniform("u_has_second_tex", True)
        else:
            self.model.texture(Null())

        self.speed = speed
        self.delay = delay

    def render(self, w, h, st, at):
        if(st < self.delay): return renpy.Render(w, h)

        anima = st*self.speed - self.delay

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
