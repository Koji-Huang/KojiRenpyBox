'''

Copyright 2025.4.23 Koji-Huang(1447396418@qq.com)

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


init python:
    renpy.register_shader("glitch",
        variables = """
            uniform float u_time;
            uniform float u_lod_bias;
            uniform vec4 u_random;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
            uniform sampler2D tex0;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_functions="""
        float make_offset(float y, float time, float random=3.1415926){
            // 将原始随机数, y 坐标, 时间进行运算获得一个随机数种子
            float x = random*20.0 + y*3.0 + time*5.0;
            // 使用三角函数获取伪噪声, 这个伪噪声就为图像的偏移值
            float primer_random = (sin(cos(x)+x) + cos(x * 0.6 + 1.5) + cos(x * 1.8 + 2.5)) / 3.0;
            // 如果偏移的绝对值小于 0.5 直接不偏移
            if(abs(primer_random)<0.5) return 0.0;
            // 否则返回偏移值的 0.1 倍
            return (primer_random / 10.0) ;
        }
        """,

        fragment_300="""
        // 获取此像素点的偏移值
        float addin = make_offset(v_tex_coord[1], u_time, u_random[0]);
        if (addin != 0.0){
            // 图像 uv 的偏移
            vec2 uv = vec2(v_tex_coord[0]+addin, v_tex_coord[1]);
            // 将图像按照偏移的 uv 进行渲染
            gl_FragColor = texture2D(tex0, uv, u_lod_bias);
            // 这里再次偏移 uv, 并分别将再次渲染的图像的 r, b 通道提取出来作为色散
            gl_FragColor.r = texture2D(tex0, vec2(uv[0] + addin / 3.0, uv[1]), u_lod_bias).r;
            gl_FragColor.b = texture2D(tex0, vec2(uv[0] - addin / 3.0, uv[1]), u_lod_bias).b;
        }
        else{
            gl_FragColor = texture2D(tex0, v_tex_coord.st, u_lod_bias);
        }
        """
    )
    
    # glitch transform
    renpy.register_shader("glitch_transform",
        variables = """
            uniform float u_time;
            uniform float u_lod_bias;
            uniform float u_renpy_dissolve;
            uniform vec4 u_random;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
            uniform sampler2D tex0;
            uniform sampler2D tex1;
        """,
        vertex_300="""
        v_tex_coord = a_tex_coord;
        """,
        fragment_functions="""
        float make_offset(float y, float time, float random=3.1415926, float offset=0.0){
            // 将原始随机数, y 坐标, 时间进行运算获得一个随机数种子
            float x = random*20.0 + y*3.0 + time*5.0;
            // 使用三角函数获取伪噪声, 这个伪噪声就为图像的偏移值
            float primer_random = (sin(cos(x)+x) + cos(x * 0.6 + 1.5) + cos(x * 1.8 + 2.5)) / 3.0;
            // 对 dissolve 的适配
            primer_random += offset * (primer_random/abs(primer_random)) * 2.0;
            // 如果偏移的绝对值小于 0.5 直接不偏移
            // if(abs(primer_random)<0.5) return 0.0;

            // 否则返回偏移值的 0.1 倍
            return primer_random;
        }
        """,
        fragment_300="""
        // 偏移的缩放
        float pos_dispersion = 0.2;
        // 色散的缩放
        float color_dispersion = 0.05;
        // 触发变化的临界值
        float dispersion_limit = 0.25;

        // 获取此像素点的偏移值
        float addin = make_offset(v_tex_coord[1], u_time, u_random[0], u_renpy_dissolve);
        // 偏移值的绝对值
        float addin_abs = abs(addin);

        // 未达到临界值, 使用原本的图像
        if(addin_abs < 0.5+dispersion_limit){
            gl_FragColor = texture2D(tex0, v_tex_coord.st, u_lod_bias);
        }
        // 达到临界值, 渲染图像
        else if(0.5+dispersion_limit <= addin_abs && addin_abs < 1.5-dispersion_limit){

            // 因为 addin 会进行修改, 新旧图像 mix 的值就提前存储了
            float mix_val = addin - 0.5;

            // 将 [0.5~1.0], [1.0~1.5] 映射为 [0.0~1.0], [1.0~0.0], 对应渐变渐出效果
            if(addin > 1.0) addin = (1.5 - addin_abs) * (addin/addin_abs);
        else addin = (addin_abs - 0.5) * (addin/addin_abs);

        // 共用一个 uv
        vec2 uv = vec2(v_tex_coord[0]+ addin * pos_dispersion, v_tex_coord[1]);
        vec2 uv_r = vec2(uv[0] + addin * color_dispersion, uv[1]);
        vec2 uv_b = vec2(uv[0] - addin * color_dispersion, uv[1]);
        
        // 渲染旧图
        vec4 bg_color = texture2D(tex0, uv, u_lod_bias);
        bg_color.r = texture2D(tex0, uv_r, u_lod_bias).r;
        bg_color.b = texture2D(tex0, uv_r, u_lod_bias).b;

        // 渲染新图
        vec4 co_color = texture2D(tex1, uv, u_lod_bias);
        co_color.r = texture2D(tex1, uv_b, u_lod_bias).r;
        co_color.b = texture2D(tex1, uv_b, u_lod_bias).b;

        // 使用 mix 函数做 dissolve
        gl_FragColor = mix(bg_color, co_color, mix_val);

    }
    // 超出临界值, 使用新图像
    else if(1.5-dispersion_limit <= addin_abs){
        gl_FragColor = texture2D(tex1, v_tex_coord.st, u_lod_bias);
    }
    """
)

    # 将 glitch 应用到可视化组件上
    def get_glitch_displayable(obj, render_size=None):
        model = Model(render_size)
        model.shader("glitch")
        model.texture(renpy.displayable(obj))
        return model


# 定义 transform
transform glitch(duration=1.0, new_widget=None, old_widget=None):
    
    delay duration
    Model().texture(old_widget).child(new_widget)

    shader ['glitch_transform']

    u_renpy_dissolve 0.0
    linear duration u_renpy_dissolve 1.0