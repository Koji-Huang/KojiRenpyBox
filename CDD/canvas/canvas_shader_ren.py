'''

Copyright 2025.6.1 Koji-Huang(koji233@163.com)

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

renpy.register_shader("draw_line", 
    variables = """
        attribute vec4 a_position;
        attribute vec2 a_tex_coord;
        uniform vec2 u_model_size;
        varying vec2 v_uv;
        varying vec2 v_position;
        varying vec2 v_coord;
        uniform vec2 u_virtual_size;
        uniform float u_lod_bias;
        uniform sampler2D tex0;
        uniform vec2 u_model_size;
        uniform vec4 u_viewport;

        uniform vec4 u_color;
        uniform float u_relat;
        uniform float u_blend;
        uniform float u_alpha;
        uniform float u_pow;

        uniform float u_round;
        uniform float u_width;
        uniform vec3 u_line;
        uniform vec3 u_triangle;
    """,
    vertex_300="""
        v_position = a_tex_coord * u_model_size;
        
        v_position.xy -= u_line.xy;
        mat2 trans = mat2(u_triangle.y, -u_triangle.x, u_triangle.x, u_triangle.y);
        v_position *= trans;
        v_coord = u_relat > 0.5 ? vec2(gl_Position.x * .5 + .5, -gl_Position.y * .5 + .5) : a_tex_coord;
    """,
    fragment_functions="""
        float count_round(vec2 uv, vec3 line, float round, float width, float val){
            # 在 x 坐标上是否处于 round 的范围内
            float half = line.z / 2.0;
            float x_cost = abs(uv.x - half) - half + round;

            if(x_cost < 0) return val;
            
            # 在 y 坐标上是否出于 round 的范围内
            float y_cost = abs(uv.y) - (width*0.5 - round);
            if(y_cost < 0.0) return val * (round - x_cost) / round;

            return (1.0 - length(vec2(x_cost, y_cost)) / round) * (round / width * 2.0);
            }
    """,
    fragment_300="""
        vec2 uv = v_position;
        float val = 0.0;
        if(0.0 < uv.x && uv.x < u_line.z && abs(uv.y) < u_width/2) { val = 1.0 - abs(uv.y) / u_width * 2.0;}
        
        if(val > 0.0 && u_round > 0.0) val = count_round(uv, u_line, u_round, u_width, val);

        if(val > 0.0) val = pow(val, u_pow);

        if(val > 0.0){
            gl_FragColor = texture2D(tex0, v_coord, u_lod_bias);
            gl_FragColor += u_color;
            gl_FragColor *= val;
        }

        gl_FragColor.rgb *= u_blend;
        gl_FragColor.a *= u_alpha;

        // gl_FragColor = vec4(v_position, 0.0, 0.0);
    """
)


renpy.register_shader("draw_rect", 
    variables = """
        attribute vec4 a_position;
        attribute vec2 a_tex_coord;
        uniform vec2 u_model_size;
        varying vec2 v_uv;
        varying vec2 v_position;
        varying vec2 v_coord;
        uniform vec2 u_virtual_size;
        uniform float u_lod_bias;
        uniform sampler2D tex0;

        uniform vec4 u_color;
        uniform float u_relat;
        uniform float u_blend;
        uniform float u_alpha;
        uniform float u_pow;

        uniform float u_round;
        uniform float u_width;
        uniform vec4 u_rect_area;
    """,
    vertex_300="""
        v_position = a_tex_coord * u_model_size;
        
        v_position.xy -= u_rect_area.xy;
        
        v_coord = u_relat > 0.5 ? vec2(gl_Position.x * .5 + .5, -gl_Position.y * .5 + .5) : a_tex_coord;
    
    """,
    fragment_functions="""
        float count_round(vec2 uv, vec2 size, float round){
            # 在 x 坐标上是否处于 round 的范围内
            vec2 half = size / 2.0;

            float x_cost = abs(uv.x - half.x);
            float y_cost = abs(uv.y - half.y);

            float x_out = (x_cost - half.x + round) / round;
            float y_out = (y_cost - half.y + round) / round;

            if(x_out < 0) x_out = 0.0;
            if(y_out < 0) y_out = 0.0;

            return 1.0 - length(vec2(x_out, y_out));

            }
    """,
    fragment_300="""
        vec2 uv = v_position;
        float val = 0.0;
        
        if(0.0 < uv.x && uv.x < u_rect_area[2] && 0.0 < uv.y && uv.y < u_rect_area[3]) {
            val = 1.0 - max(abs(uv.x - u_rect_area[2]/2) / u_rect_area[2] * 2, abs(uv.y - u_rect_area[3]/2) / u_rect_area[3] * 2);
        }
            
        
        if(val > 0 && u_round > 0) val = count_round(uv, u_rect_area.zw, u_round);
        
        if(u_width > 0){
            if(u_round > 0) {
                float m = u_width / u_round;
                if(0 < val && val < m) val = 1.0 - abs(val - m/2) / m * 2;
                else val = 0.0;
            }
            else {
                float x_cost = abs(uv.x - u_rect_area.z/2.0) - u_rect_area.z/2.0 + u_width;
                float y_cost = abs(uv.y - u_rect_area.w/2.0) - u_rect_area.w/2.0 + u_width;
                if(x_cost < 0) x_cost = 0.0;
                else x_cost = 1.0 - abs(x_cost / u_width - 0.5) * 2;
                if(y_cost < 0) y_cost = 0.0;
                else y_cost = 1.0 - abs(y_cost / u_width - 0.5) * 2;
                if(abs(uv.y - u_rect_area.w/2.0) + u_width/2 > (u_rect_area.w) / 2) x_cost *= y_cost;
                if(abs(uv.x - u_rect_area.z/2.0) + u_width/2 > (u_rect_area.z) / 2) y_cost *= x_cost;

                val = x_cost + y_cost - min(x_cost, y_cost);
            }
            
        }

        val = pow(val, u_pow);

        if(val > 0.0){
            gl_FragColor = texture2D(tex0, v_coord, u_lod_bias);
            gl_FragColor += u_color;
            gl_FragColor *= val;
        }

        gl_FragColor.rgb *= u_blend;
        gl_FragColor.a *= u_alpha;

        // gl_FragColor = vec4(val, 0.0, 0.0, 0.0);
    """
) 


renpy.register_shader("draw_circle", 
    variables = """
        attribute vec4 a_position;
        attribute vec2 a_tex_coord;
        uniform vec2 u_model_size;
        varying vec2 v_uv;
        varying vec2 v_position;
        varying vec2 v_coord;
        uniform vec2 u_virtual_size;
        uniform float u_lod_bias;
        uniform sampler2D tex0;

        uniform vec4 u_color;
        uniform float u_relat;
        uniform float u_blend;
        uniform float u_alpha;
        uniform float u_pow;

        uniform vec2 u_pos;
        uniform float u_r;
        uniform float u_width;
        uniform vec2 u_degree;
        uniform float u_round;
    """,
    vertex_300="""
        v_position = a_tex_coord * u_model_size;
        
        v_position.xy -= u_pos.xy;

        v_coord = u_relat > 0.5 ? vec2(gl_Position.x * .5 + .5, -gl_Position.y * .5 + .5) : a_tex_coord;
    
    """,
    fragment_functions="""
        float count_round(vec2 uv, float len, float round, float width, float val){
            # 在 x 坐标上是否处于 round 的范围内
            float half = len / 2.0;
            float x_cost = abs(uv.x - half) - half + round;

            if(x_cost < 0) return val;
            
            # 在 y 坐标上是否出于 round 的范围内
            float y_cost = abs(uv.y) - (width*0.5 - round);
            if(y_cost < 0.0) return val * (round - x_cost) / round;
            // return x_cost / round;
            // return y_cost;
            // return (1.0 - length(vec2(x_cost / round, y_cost / width)));
            

            return (1.0 - length(vec2(x_cost, y_cost)) / round) * (round / width);
            }
    """,
    fragment_300="""
        vec2 uv = v_position;
        
        float degree = atan(uv.x, uv.y)-u_degree.x;
        degree = fract(degree / 3.1415926 / 2.0) * 3.1415926 * 2; 

        float dis = length(uv);

        float val = 0.0;

        if(u_width > 0.0) {
            if(u_r - u_width/2.0 < dis && dis < u_r + u_width/2.0){ 
                val = 1.0 - sqrt((abs(dis-u_r) / u_width * 2.0));
            };
        }
        else if(u_r > dis) val = 1.0 - dis / u_r;

        if(val > 0.0 && u_degree.y < 3.1415926 * 2.0){
            if(0 < degree && degree < u_degree.y) {
                if(u_width > 0.0)
                    val = count_round(
                        vec2((degree) * u_r, u_r-dis), 
                        abs(u_degree.y) * u_r, 
                        u_round, 
                        u_width, 
                        val);
                }
                
            else val = 0.0;
        }
        val = pow(val, u_pow);

        if(val > 0.0){
            gl_FragColor = texture2D(tex0, v_coord, u_lod_bias);
            gl_FragColor += u_color;
            gl_FragColor *= val;
         }

         gl_FragColor.rgb *= u_blend;
         gl_FragColor.a *= u_alpha;
        // gl_FragColor = vec4(val, 0.0, 0.0, 0.0);
    """
)

