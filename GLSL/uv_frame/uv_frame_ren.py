"""renpy

python early:
"""

renpy.register_shader("uv_apply", 
    variables="""
        uniform float u_lod_bias;
        uniform sampler2D tex0;
        uniform sampler2D tex1;
        uniform float u_sample_dis;
        uniform float u_sample_level;
        uniform float u_alpha_pow;
        uniform float u_only_uv;
        uniform float u_blend_alpha;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """,
    vertex_300="""
        v_tex_coord = a_tex_coord;
    """,
    fragment_functions="""

        vec4 sample_5(sampler2D uv_image, vec2 coord, float lod, float dis){
            vec4 uv = vec4(0.0, 0.0, 0.0, 0.0);
            uv += texture2D(uv_image, vec2(coord.x, coord.y), lod) * (1.0 / 5.0);
            uv += texture2D(uv_image, vec2(coord.x + dis, coord.y + dis), lod) * (1.0 / 5.0);
            uv += texture2D(uv_image, vec2(coord.x - dis, coord.y + dis), lod) * (1.0 / 5.0);
            uv += texture2D(uv_image, vec2(coord.x + dis, coord.y - dis), lod) * (1.0 / 5.0);
            uv += texture2D(uv_image, vec2(coord.x - dis, coord.y - dis), lod) * (1.0 / 5.0);
            return uv;
        }

        vec4 sample_9(sampler2D uv_image, vec2 coord, float lod, float dis){
            vec4 uv = vec4(0.0, 0.0, 0.0, 0.0);

            uv += texture2D(uv_image, vec2(coord.x, coord.y), lod) * (1.0 / 9.0);
            uv += texture2D(uv_image, vec2(coord.x + dis / 2.0, coord.y + dis / 2.0), lod) * (1.0 / 9.0);
            uv += texture2D(uv_image, vec2(coord.x - dis / 2.0, coord.y + dis / 2.0), lod) * (1.0 / 9.0);
            uv += texture2D(uv_image, vec2(coord.x + dis / 2.0, coord.y - dis / 2.0), lod) * (1.0 / 9.0);
            uv += texture2D(uv_image, vec2(coord.x - dis / 2.0, coord.y - dis / 2.0), lod) * (1.0 / 9.0);
            uv += texture2D(uv_image, vec2(coord.x + dis, coord.y), lod) * (1.0 / 9.0);
            uv += texture2D(uv_image, vec2(coord.x - dis, coord.y), lod) * (1.0 / 9.0);
            uv += texture2D(uv_image, vec2(coord.x, coord.y + dis), lod) * (1.0 / 9.0);
            uv += texture2D(uv_image, vec2(coord.x, coord.y - dis), lod) * (1.0 / 9.0);
            return uv;
        }

        vec4 sample_circle_20(sampler2D uv_image, vec2 coord, float lod, float dis){
            float times_a = 10;
            float time = 1.0 / (times_a * 2.0 + 1);
            vec4 uv = vec4(0.0, 0.0, 0.0, 0.0);
            uv += texture2D(uv_image, coord, lod) * time;

            for(int i=0; i < times_a; i++){
                vec2 offset = vec2(sin(i / 20.0 * 3.1415 * 2), cos(i / 20.0 * 3.1415 * 2));
                uv += texture2D(uv_image, coord + offset * dis / 2.0, lod) * time;
                uv += texture2D(uv_image, coord + offset * dis, lod) * time;
            }

            return uv;
        }

        vec4 sample_circle_40(sampler2D uv_image, vec2 coord, float lod, float dis){
            float times_a = 20;
            float time = 1.0 / (times_a * 2.0 + 1);
            vec4 uv = vec4(0.0, 0.0, 0.0, 0.0);
            uv += texture2D(uv_image, coord, lod) * time;

            for(int i=0; i < times_a; i++){
                vec2 offset = vec2(sin(i / 20.0 * 3.1415 * 2), cos(i / 20.0 * 3.1415 * 2));
                uv += texture2D(uv_image, coord + offset * dis / 2.0, lod) * time;
                uv += texture2D(uv_image, coord + offset * dis, lod) * time;
            }

            return uv;
        }

        vec4 sample_circle_60(sampler2D uv_image, vec2 coord, float lod, float dis){
            float times_a = 20;
            float time = 1.0 / (times_a * 3.0 + 1);
            vec4 uv = vec4(0.0, 0.0, 0.0, 0.0);
            uv += texture2D(uv_image, coord, lod) * time;

            for(int i=0; i < times_a; i++){
                vec2 offset = vec2(sin(i / 20.0 * 3.1415 * 2), cos(i / 20.0 * 3.1415 * 2));
                uv += texture2D(uv_image, coord + offset * dis / 3.0, lod) * time;
                uv += texture2D(uv_image, coord + offset * dis / 2.0, lod) * time;
                uv += texture2D(uv_image, coord + offset * dis, lod) * time;
            }

            return uv;
        }

        vec4 sample_circle_90(sampler2D uv_image, vec2 coord, float lod, float dis){
            float times_a = 30;
            float time = 1.0 / (times_a * 3.0 + 1);
            vec4 uv = vec4(0.0, 0.0, 0.0, 0.0);
            uv += texture2D(uv_image, coord, lod) * time;

            for(int i=0; i < times_a; i++){
                vec2 offset = vec2(sin(i / 20.0 * 3.1415 * 2), cos(i / 20.0 * 3.1415 * 2));
                uv += texture2D(uv_image, coord + offset * dis*0.3, lod) * time;
                uv += texture2D(uv_image, coord + offset * dis*0.5, lod) * time;
                uv += texture2D(uv_image, coord + offset * dis, lod) * time;
            }

            return uv;
        }

    """,
    fragment_300="""
        vec4 uv = vec4(0.0, 0.0, 0.0, 0.0);

        switch(int(u_sample_level)){
            case 0: 
                uv = texture2D(tex1, v_tex_coord, u_lod_bias);
                break;
            case 1: 
                uv = sample_5(tex1, v_tex_coord, u_lod_bias, u_sample_dis); 
                break;
            case 2: 
                uv = sample_9(tex1, v_tex_coord, u_lod_bias, u_sample_dis); 
                break;
            case 3: 
                uv = sample_circle_20(tex1, v_tex_coord, u_lod_bias, u_sample_dis); 
                break;
            case 4: 
                uv = sample_circle_40(tex1, v_tex_coord, u_lod_bias, u_sample_dis); 
                break;
            case 5: 
                uv = sample_circle_60(tex1, v_tex_coord, u_lod_bias, u_sample_dis); 
                break;
            case 6: 
                uv = sample_circle_90(tex1, v_tex_coord, u_lod_bias, u_sample_dis); 
                break;
            default:
                uv = sample_circle_20(tex1, v_tex_coord, u_lod_bias, u_sample_dis); 
                break;
        }
        vec4 color = texture2D(tex0, uv.xy / uv.a, 1.0);
        if(u_blend_alpha < 0.5) uv.a = texture2D(tex1, v_tex_coord, u_lod_bias).a;
        uv.a = pow(uv.a, u_alpha_pow);
        if(u_only_uv < 0.5) gl_FragColor = vec4(color.rgb*uv.a, uv.a);
        else gl_FragColor = uv;
    """
    )


# 将单个 UV 作用到 image 上
class SingleUV_Frame(renpy.Displayable):
    def __init__(self, image, uv, sample_dis=0.005, sample_level=3.0, alpha_pow=3, load_cache=True, render_image_size=True, anisotropic=True, blend_alpha=False, only_uv=False):
        super().__init__()
        self.image = renpy.displayable(image)
        self.model = Model()
        self.model.shader("uv_apply")
        self.model.property("gl_anisotropic", anisotropic)
        self.model.uniform("u_sample_dis", sample_dis)
        self.model.uniform("u_sample_level", sample_level)
        self.model.uniform("u_alpha_pow", alpha_pow)
        self.model.uniform("u_only_uv", only_uv)
        self.model.uniform("u_blend_alpha", blend_alpha)
        self.model.texture(self.image)
        self.model.texture(uv)
        self.render_image_size = render_image_size
        if load_cache: self.model.render(0, 0, 0, 0)

    def render(self, w, h, st, at):
        if self.render_image_size:
            w, h = self.image.render(w, h, st, at).get_size()
        return self.model.render(w, h, st, at)


# 将多个 UV 作用到 image 上
# 注意 load_cache 参数, 这个参数为 True 时会强制加载好所有的 uv 来保证后面的动画流畅
class AnimaUV_Frame(renpy.Displayable):
    def __init__(self, image, uv_files, anima_loop_time=1.0, sample_dis=0.003, sample_level=3.0, alpha_pow=1, load_cache=True, render_image_size=True, anisotropic=True, blend_alpha=False,  only_uv=False):
        super().__init__()
        self.image = renpy.displayable(image)
        self.time = anima_loop_time
        self.uv = tuple(renpy.displayable(i) for i in uv_files)
        self.model = []
        for i in range(self.uv.__len__()):
            model = Model()
            model.shader("uv_apply")
            model.property("gl_anisotropic", anisotropic)
            model.uniform("u_sample_dis", sample_dis)
            model.uniform("u_sample_level", sample_level)
            model.uniform("u_alpha_pow", alpha_pow)
            model.uniform("u_only_uv", only_uv)
            model.uniform("u_blend_alpha", blend_alpha)
            model.texture(self.image)
            model.texture(self.uv[i])
            if load_cache: model.render(0, 0, 0, 0)
            self.model.append(model)
        self.frame = 0.0
        self.render_image_size = render_image_size

    def render(self, w, h, st, at):
        self.frame = int((st / self.time) * self.uv.__len__()) % self.uv.__len__()
        if self.render_image_size:
            w, h = self.image.render(w, h, st, at).get_size()
        renpy.redraw(self, 0)
        return self.model[self.frame].render(w, h, st, at)

