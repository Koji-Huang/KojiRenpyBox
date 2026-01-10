'''

Copyright 2026.1.8 Koji-Huang(1447396418@qq.com)

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

python early:
"""

# Transform Shader
renpy.register_shader("trailing_glitch",
    variables = """
        uniform float u_time;
        uniform float u_lod_bias;
        uniform vec4 u_random;
        uniform float u_weight;
        uniform float u_color_weight;
        uniform vec2 u_angle;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform sampler2D tex0;
    """,
    vertex_300="""
    v_tex_coord = a_tex_coord;
    """,
    fragment_functions="""
    float PI = 3.14159265358979;

    //	<https://www.shadertoy.com/view/4dS3Wd>
    //	By Morgan McGuire @morgan3d, http://graphicscodex.com
    //
    float hash(float n) { return fract(sin(n) * 1e4); }
    float hash(vec2 p) { return fract(1e4 * sin(17.0 * p.x + p.y * 0.1) * (0.1 + abs(sin(p.y * 13.0 + p.x)))); }

    //1D
    float noise(float x) {
        float i = floor(x);
        float f = fract(x);
        float u = f * f * (3.0 - 2.0 * f);
        return mix(hash(i), hash(i + 1.0), u);
    }

    
    // 评估色差做参考
    float value_color_diff(vec4 col1, vec4 col2){
        col1.rgb = col1.rgb * col1.a;
        col2.rgb = col2.rgb * col2.a;
        return (abs(col1.r-col2.r) + abs(col1.g - col2.g) + abs(col1.b - col2.b))/3.0;
    }

    // 根据匹配数据排序索引
    int[3] sort_trailing(float number[3]){
        int head, end;
        if(number[0]>number[1]){
            if(number[0]>number[2]){
                head = 0;
                end = 2;
            }
            else{
                head = 2;
                end = 0;
            }
        }   
        else{
            if(number[1]>number[2]){
                head = 1;
                end = (number[0]>number[2])?2:0;
            }
            else{
                head = 2;
                end = 0;
            }
        }

        return int[3](head, 3-head-end, end);
    }

    // 区块匹配
    vec2[3] get_trailing(vec2 start, vec2 end, vec4 ori_color, sampler2D tex, float bias){

        vec2[] trailing = vec2[](start, mix(start, end, 0.5), end);

        vec4 color[] = vec4[](
            texture2D(tex, trailing[0], bias), 
            texture2D(tex, trailing[1], bias), 
            texture2D(tex, trailing[2], bias)
        );

        float differ[] = float[](
            value_color_diff(color[0], ori_color), 
            value_color_diff(color[1], ori_color), 
            value_color_diff(color[2], ori_color), 
            value_color_diff(color[0], color[1]), 
            value_color_diff(color[1], color[2])
        );

        float number[] = float[](
            differ[0]*1.0 + (1.0 - differ[3])*1.5 + 0.4,
            differ[1]*1.0 + (1.0 - max(differ[3], differ[4]))*1.5 + 0.3,
            differ[2]*1.0 + (1.0 - differ[4])*1.5 + 0.2
        );
        
        int sort[3] = sort_trailing(number);

        return vec2[3](trailing[sort[0]], trailing[sort[1]], trailing[sort[2]]);
    }

    // 渐变着色
    vec4 multi_sample(vec2 start, vec2 end, sampler2D tex, float bias){
        vec4 color = texture2D(tex, start, bias);
        color = mix(color, texture2D(tex, mix(start, end, 0.2), bias), 0.3);
        color = mix(color, texture2D(tex, mix(start, end, 0.5), bias), 0.2);
        color = mix(color, texture2D(tex, mix(start, end, 0.8), bias), 0.1);
        return color;
    }

    vec4 mix_shade(vec2[3] trailing, vec4 ori_color, sampler2D tex, float bias, vec2 offset){
        return (texture2D(tex, trailing[0]+offset, bias)*0.6 + texture2D(tex, trailing[1]+offset, bias)*0.2 + texture2D(tex, trailing[2]+offset, bias)*0.1 + ori_color*0.1);
    }    

    vec4 darken_blend(vec4 col1, vec4 col2){
        return vec4(min(col1.r, col2.r), min(col1.g, col2.g), min(col1.b, col2.b), (col1.a+col2.a)/2.0);
    }

    """,

    fragment_300="""
        
        vec2 uv = v_tex_coord;

        // 屏幕抖动效果 ( 可开启, 这里注释掉是方便了解基础效果 )
        // uv += vec2(noise(v_tex_coord.x+u_time*1000)*0.01, noise(v_tex_coord.y+u_time*1000)*0.01); 

        // 起始点
        vec2 start = uv;

        // 对起始采样点进行噪波处理, 可以让画面更可怕 ( 可开启, 这里注释掉是方便了解基础效果 )
        // start += vec2(noise((uv.x+u_time)*10000), noise((uv.y+u_time)*10000))*0.01;

        vec2 trans_v = vec2((u_angle[1] -u_angle[0]), (u_angle[0] + u_angle[1]));
        mat2 trans_m = mat2(u_angle[1], -u_angle[0],  u_angle[0], u_angle[1]);
        vec2 trans_pos = trans_v * uv;

        // 需要正反两个方向偏移的话把 abs 删掉就好
        vec2 offset = trans_m * vec2(-vec2(abs(noise(mod(trans_pos.y + u_time, 17.0)*15760))*0.2 + abs(noise(mod(trans_pos.y + u_random[0]*1000, 17.0)*15))*(abs(noise(u_time*10000.0))), 0.0)*u_weight);

        vec2 end = start + offset;

        vec4 ori_color = texture2D(tex0, uv, u_lod_bias);
        // 偏移采样
        ori_color = darken_blend(ori_color, texture2D(tex0, vec2(uv.x+noise(u_time*10)*0.03, uv.y+noise(u_time*10)*0.03), u_lod_bias));
        ori_color = darken_blend(ori_color, texture2D(tex0, vec2(uv.x+noise(u_time*10)*0.03, uv.y+noise(u_time*13)*0.03), u_lod_bias));


        /////////////////////////
        // 区块查找
        vec2[3] trailing = vec2[3](start, end, vec2(0.0, 0.0));
        
        // 强化查找
        trailing = get_trailing(trailing[0], trailing[1], ori_color, tex0, u_lod_bias);
        trailing = get_trailing(trailing[0], trailing[1], ori_color, tex0, u_lod_bias);
        trailing = get_trailing(trailing[0], trailing[1], ori_color, tex0, u_lod_bias);

        

        ///////////////////////////////
        // 着色区
        // 写爽了随便多写几个玩
        // 所谓的色散就是里面写死且重复的 vec2(0.01, 0.0)
        // 想让色散分布的更不平均可以让 texture2D 中每个通道的 uv: trailing[0], trailing[0], trailing[0] 变成 trailing[0], trailing[1], trailing[2]

        // 最佳匹配着色
        // gl_FragColor = (texture2D(tex0, trailing[0], u_lod_bias));

        // 色散最佳匹配着色
        gl_FragColor = vec4(
            texture2D(tex0, trailing[0]+u_color_weight*vec2(0.01, 0.0)*trans_m, u_lod_bias).r, 
            texture2D(tex0, trailing[0]+u_color_weight*vec2(0.00, 0.0)*trans_m, u_lod_bias).g, 
            texture2D(tex0, trailing[0]-u_color_weight*vec2(0.01, 0.0)*trans_m, u_lod_bias).b, 
            ori_color.a);

        // 混合着色
        // gl_FragColor = mix_shade(trailing, ori_color, tex0, u_lod_bias, vec2(0.0, 0.0));
        // gl_FragColor = vec4(
        //     mix_shade(trailing, ori_color, tex0, u_lod_bias, u_color_weight * vec2(0.01, 0.0)).r,
        //     mix_shade(trailing, ori_color, tex0, u_lod_bias, u_color_weight * vec2(0.00, 0.0)).g,
        //     mix_shade(trailing, ori_color, tex0, u_lod_bias, u_color_weight * vec2(-0.01, 0.0)).b,
        //     ori_color.a
        //     );

        // 渐变着色
        // gl_FragColor = multi_sample(trailing[0], start, tex0, u_lod_bias);

        // 色散渐变着色
        // gl_FragColor = vec4(
        //     multi_sample(trailing[0]+u_color_weight*vec2(0.01, 0.0)*trans_m, start, tex0, u_lod_bias).r, 
        //     multi_sample(trailing[0]+u_color_weight*vec2(0.00, 0.0)*trans_m, start, tex0, u_lod_bias).g, 
        //     multi_sample(trailing[0]-u_color_weight*vec2(0.01, 0.0)*trans_m, start, tex0, u_lod_bias).b, 
        //     ori_color.a);
        

        // DEBUG
        // gl_FragColor = texture2D(tex0, trailing[0], u_lod_bias);
        // gl_FragColor = vec4(start.x-end.x, start.y-end.y, 0.0, 1.0);
        // gl_FragColor = vec4(abs(trailing[0].x-start.x), abs(trailing[0].y-end.y), 0.0, 1.0);
        // gl_FragColor = ori_color;
    """
)


class TrailingGlitch(renpy.Container):
    def __init__(self, child=None, weight=0.5, color_weight=0.5, angle=0, always_update=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.child = child
        self.model = None
        self.weight = weight
        self.color_weight = color_weight
        self.angle = angle
        self.always_update = always_update
        self.reset_model()

    def reset_model(self):
        self.model = Model()
        self.model.shader("trailing_glitch")
        self.model.uniform("u_weight", self.weight)
        self.model.uniform("u_color_weight", self.color_weight)
        self.model.uniform("u_angle", (sin(self.angle), cos(self.angle)))
        if self.child is not None:
            self.model.texture(self.child)
    
    def render(self, w, h, st, at):
        rend = renpy.render(self.model, w, h, st, at)
        if self.always_update:
            renpy.redraw(self, 0)
        return rend

    def add(self, child):
        super().add(child)
        self.reset_model()

    def remove(self, child):
        super().add(child)
        self.reset_model()

    def update(self):
        super().update()
        self.reset_model()

    def _clear(self):
        super()._clear()
        self.reset_model()


renpy.register_sl_displayable("trailing_glitch", TrailingGlitch, "", 1
    ).add_property("always_update"
    ).add_property("weight"
    ).add_property("color_weight"
    ).add_property("angle"
    ).add_property_group("position")



"""renpy

# 定义 transform
transform trailing_glitch(weight, color_weight, angle):
    mesh True
    shader ['trailing_glitch']
    u_weight weight
    u_color_weight color_weight
    u_angle (sin(angle), cos(angle))
"""