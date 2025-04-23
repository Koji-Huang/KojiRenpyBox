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


"""renpy

python early:
"""

renpy.register_shader("one_point_perspective",
    variables="""
        uniform float u_intensity;
        uniform float u_lod_bias;

        uniform vec2 u_mask_center;
        uniform vec4 u_mask_area;

        uniform vec2 u_center;
        uniform vec4 u_area;

        uniform vec4 u_ignore_area;
        uniform float u_ignore_center;

        uniform float u_enable_debug;

        uniform sampler2D tex0;

        varying vec2 v_tex_coord;
        varying vec2 v_center;
        varying vec4 v_area_k;

        attribute vec2 a_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;

        // 真实的中心点
        v_center = vec2(mix(u_area[0], u_area[1], u_center.x), mix(u_area[2], u_area[3], u_center.y));

        // 矩阵区域检测用
        vec2 k_a = (v_center - vec2(u_area[0], u_area[2]));
        vec2 k_b = (v_center - vec2(u_area[1], u_area[2]));
        vec2 k_c = (v_center - vec2(u_area[0], u_area[3]));
        vec2 k_d = (v_center - vec2(u_area[1], u_area[3]));
        v_area_k = vec4(k_a.x/k_a.y, k_b.x/k_b.y, k_c.x/k_c.y, k_d.x/k_d.y);
    """,
    fragment_functions="""
        float right_dis(vec2 coord, vec4 area, vec2 center, int choose){

            vec4 dist = vec4(abs(area[0] - center[0]), abs(area[1] - center[0]), abs(area[2] - center[1]), abs(area[3] - center[1]));

            bool left = (coord.x < (area[0] + area[1])/2), top = (coord.y < (area[2] + area[3])/2);

            if((area[0] <= coord.x && coord.x <= area[1]) || (area[2] <= coord.y && coord.y <= area[3])){
                if(choose==0) return abs(coord.x - area[0]) / dist[0];
                if(choose==1) return abs(coord.x - area[1]) / dist[1];
                if(choose==2) return abs(coord.y - area[2]) / dist[2];
                if(choose==3) return abs(coord.y - area[3]) / dist[3];
            }

            if (left && top)    return max(abs(coord.x - area[0]) / dist[0], abs(coord.y - area[2]) / dist[2]);
            if (left && !top)   return max(abs(coord.x - area[0]) / dist[0], abs(coord.y - area[3]) / dist[3]);
            if (!left && top)   return max(abs(coord.x - area[1]) / dist[1], abs(coord.y - area[2]) / dist[2]);
            if (!left && !top)  return max(abs(coord.x - area[1]) / dist[1], abs(coord.y - area[3]) / dist[3]);

        }

        bool get_area(vec2 obj, float k1, float k2){
            float k = obj.x/obj.y;
            if(k1 > k2) return (k1 >= k && k >= k2);
            else return (k1 <= k && k <= k2);
        }
    """,
    fragment_300="""

        if (u_area[0] <= v_tex_coord.x && v_tex_coord.x <= u_area[1] && u_area[2] <= v_tex_coord.y && v_tex_coord.y <= u_area[3]){

            if(u_ignore_center > 0.5){
                gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
            }

            else{
                vec2 percent_uv = (v_tex_coord-u_area.xz)/(u_area.yw-u_area.xz);
                vec2 uv = mix(u_mask_area.xz, u_mask_area.yw, percent_uv);

                gl_FragColor = texture2D(tex0, uv, u_lod_bias);
            }

            if (u_enable_debug==1.0){
                if (length(v_tex_coord-v_center) < 0.003) gl_FragColor *= 2.0;
                if (length(v_tex_coord-v_center) < 0.002) gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0) - gl_FragColor;
                }
            }
        else{
            vec2 coord = v_tex_coord;

            int choose = 0;
            bool y_state = v_center.y < coord.y, x_state = v_center.x < coord.x;
            float k = (v_center.x - coord.x) / (v_center.y - coord.y);

            // choose: 0 左边, 1 右边, 2 上面, 3 下面

            if(y_state && x_state)   {if(k < v_area_k[3]) choose = 3; else choose = 1;}
            if(y_state && !x_state)  {if(k > v_area_k[2]) choose = 3; else choose = 0;}
            if(!y_state && x_state)  {if(k > v_area_k[1]) choose = 2; else choose = 1;}
            if(!y_state && !x_state) {if(k < v_area_k[0]) choose = 2; else choose = 0;}

            if (u_ignore_area[choose] > 0.5){
                gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
            }

            else{
                
                float p = 0.0;
                vec2 b = vec2(0.0, 0.0);

                if(choose == 0) {
                    float ay = -(v_center.x - u_area[0]) / k + v_center.y;
                    p = (ay - u_area[2]) / (u_area[3] - u_area[2]);
                    b = vec2(u_mask_area[0], mix(u_mask_area[2],  u_mask_area[3], p));
                }
                if(choose == 1) {
                    float ay = -(v_center.x - u_area[1]) / k + v_center.y;
                    p = (ay - u_area[2]) / (u_area[3] - u_area[2]);
                    b = vec2(u_mask_area[1], mix(u_mask_area[2],  u_mask_area[3], p));
                }
                if(choose == 2)  {
                    float ax = (u_area[2] - v_center.y) * k + v_center.x;
                    p = (ax - u_area[0]) / (u_area[1] - u_area[0]);
                    b = vec2(mix(u_mask_area[0],  u_mask_area[1], p), u_mask_area[2]);
                }
                if(choose == 3) {
                    float ax = (u_area[3] - v_center.y) * k + v_center.x;
                    p = (ax - u_area[0]) / (u_area[1] - u_area[0]);
                    b = vec2(mix(u_mask_area[0],  u_mask_area[1], p), u_mask_area[3]);
                }

                float dis = right_dis(coord, u_area, v_center, choose);
                
                vec2 real_mask_center = vec2(mix(u_mask_area[0], u_mask_area[1], u_mask_center.x), mix(u_mask_area[2], u_mask_area[3], u_mask_center.y));

                vec2 uv = b + (b - real_mask_center) * dis * u_intensity;

                if (0.0 <= uv.x && uv.x <= 1.0 && 0.0 <= uv.y && uv.y <= 1.0) gl_FragColor = texture2D(tex0, uv, u_lod_bias);
                else gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);

                if(u_enable_debug==1.0){
                    if (choose == 0) gl_FragColor += 0.15 * vec4(1.0, 0.0, 0.0, 1.0);
                    if (choose == 1) gl_FragColor += 0.15 * vec4(0.0, 1.0, 0.0, 1.0);
                    if (choose == 2) gl_FragColor += 0.15 * vec4(0.0, 0.0, 1.0, 1.0);
                    if (choose == 3) gl_FragColor += 0.15 * vec4(0.5, 0.5, 0.5, 1.0);
                }
            }

            
        }
    """
)


from typing import Iterable
    

class OnePointPerspective(renpy.Displayable):
    def __init__(self, 
            texture, 
            mask_center=(0.5, 0.5), 
            mask_area=(0.4, 0.6, 0.4, 0.6), 
            center=None, 
            area=None, 
            intensity=1.0, 
            render_size=None, 
            always_update=True, 
            enable_debug=False, 
            ignore_area = (False, False, False, False),
            ignore_center = False,
            addin=()):
        super().__init__()
        self.model = Model(render_size)
        self.model.shader("one_point_perspective")
        self.model.texture(texture)

        self.ignore_area = ignore_area
        self.ignore_center = ignore_center
        
        self.mask_center = mask_center
        self.mask_area = mask_area
        self.center = center if center is not None else mask_center
        self.area = area if area is not None else mask_area
        self.intensity = intensity

        self._center = self.center
        self._area = self.area
        self._mask_center = self.mask_center
        self._mask_area = self.mask_area
        self._intensity = self.intensity

        self.enable_debug = enable_debug
        self.always_update = always_update
        self.uniform = self.model.uniform
        self.addin = addin
        self.olds = None

        self.reset_arg()
        self.save_old_arg()
        self.update_uniform(force=True)

    def set_basic_val(self, center=None, area=None, mask_center=None, mask_area=None, intensity=None):
        self._center = center if center is not None else self._center
        self._area = area if area is not None else self._area
        self._mask_center = mask_center if mask_center is not None else self._mask_center
        self._mask_area = mask_area if mask_area is not None else self._mask_area
        self._intensity = intensity if intensity is not None else self._intensity
    
    def save_old_arg(self):
        self.olds = (self.center, self.area, self.mask_center, self.mask_area, self.intensity, self.enable_debug, self.ignore_area, self.ignore_center)
    
    def reset_arg(self):
        self.center = self._center
        self.area = self._area
        self.mask_center = self._mask_center
        self.mask_area = self._mask_area
        self.intensity = self._intensity
    
    def render(self, w, h, st, at):

        if self.always_update:
            renpy.redraw(self, 0)
            renpy.redraw(self.model, 0)
        for i in self.addin if isinstance(self.addin, Iterable) else (self.addin, ):
            i.render(self, w, h, st, at)

        self.update_uniform()
        
        self.save_old_arg()

        return renpy.render(self.model, w, h, st, at)

    def update_uniform(self, force=False):

        if force or self.olds[0] != self.center:
            self.model.uniform("u_center", self.center)
        if force or self.olds[1] != self.area:
            self.model.uniform("u_area", self.area)
        if force or self.olds[2] != self.mask_center:
            self.model.uniform("u_mask_center", self.mask_center)
        if force or self.olds[3] != self.mask_area:
            self.model.uniform("u_mask_area", self.mask_area)
        if force or self.olds[4] != self.intensity:
            self.model.uniform("u_intensity", self.intensity)
        if force or self.olds[5] != self.enable_debug:
            self.model.uniform("u_enable_debug", self.enable_debug*1.0)
        if force or self.olds[6] != self.ignore_area:
            self.model.uniform("u_ignore_area", tuple(i*1.0 for i in self.ignore_area))
        if force or self.olds[7] != self.ignore_center:
            self.model.uniform("u_ignore_center", self.ignore_center*1.0)
    
    def event(self, ev, x, y, st):
        for i in self.addin if isinstance(self.addin, Iterable) else (self.addin, ):
            i.event(self, ev, x, y, st)
            
        return self.model.event(ev, x, y, st)

