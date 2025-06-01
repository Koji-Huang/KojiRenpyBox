"""renpy

init python:
"""
from typing import Iterable
from math import atan2, sin, cos, pi

def choose_val(a, b):
    return a if a is not None else b

def TT_sub_2(a, b):
    return (a[0]-b[0], a[1]-b[1])
    
def TT_dis(vec):
    return sqrt(pow(vec[0], 2) + pow(vec[1], 2))

def line_pixel(node_a, node_b):
    return node_a[0], node_b[0], TT_dis(sub)


class InfoObj:
    def __init__(self):
        pass

    def init_model(self, model, **kwargs):
        self.apply_uniform(model, **kwargs)
    
    def apply_uniform(self, model, **kwargs):
        if isinstance(model, Iterable) is False:
            model = (model, )

        for target in model:
            for key, val in kwargs.items():
                target.uniform(key, val)
        
    def __copy__(self):
        return InfoObj()


class TextureInfo(InfoObj):
    def __init__(self, displayable=None, color=None, alpha=1.0, blend=1.0, val_pow=0.1, relative_coord=True):
        super().__init__()
        self.displayable = displayable
        if displayable is not None:
            self.color = choose_val(color, (0.0, 0.0, 0.0, 0.0))
        else:
            self.color = choose_val(color, (1.0, 1.0, 1.0, 0.0))
        self.alpha = alpha
        self.blend = blend
        self.pow = val_pow
        self.relative_coord = relative_coord

    def init_model(self, model, **kwargs):
        super().init_model(model, **kwargs)
        if self.displayable is None:
            self.displayable = Null()
        model.child(self.displayable)
    
    def apply_uniform(self, model, **kwargs):
        super().apply_uniform(
            model, 
            u_color=self.color, 
            u_alpha=self.alpha, 
            u_blend=self.blend, 
            u_pow=self.pow, 
            u_relat=self.relative_coord,
            **kwargs)
    
    def __copy__(self, displayable=None, color=None, alpha=None, blend=None, val_pow=None, relative_coord=None):
        return TextureInfo(
                displayable=choose_val(displayable, self.displayable), 
                color=choose_val(color, self.color[:]), 
                alpha=choose_val(alpha, self.alpha), 
                blend=choose_val(blend, self.blend),
                val_pow=choose_val(val_pow, self.pow),
                relative_coord=choose_val(relative_coord, self.relative_coord),
            )


class WithTextureInfo(InfoObj):
    def __init__(self, texture=None):
        self.texture = texture if texture is not None else TextureInfo()

    def init_model(self, model, **kwargs):
        self.texture.init_model(model, **kwargs)
        super().init_model(model, **kwargs)

    def apply_uniform(self, model, **kwargs):
        self.texture.apply_uniform(model)
        super().apply_uniform(model, **kwargs)

    def __copy__(self, texture=None):
        return WithTextureInfo(
            choose_val(texture, self.texture.__copy__())
            )



class LineInfo(WithTextureInfo):
    def __init__(self, start_pos, end_pos, width=10, round=0.0, texture=None):
        super().__init__(texture)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
        self.round = round

    def apply_uniform(self, model, **kwargs):
        start_pos = self.start_pos
        end_pos = self.end_pos

        if start_pos[1] == end_pos[1]:
            end_pos = end_pos[0], start_pos[1] + 0.00001
        if start_pos[0] > end_pos[0]:
            start_pos, end_pos = end_pos, start_pos

        sub = TT_sub_2(end_pos, start_pos)
        degree = atan2(*sub) - pi / 2

        super().apply_uniform(
            model, 
            u_line=(*start_pos, TT_dis(sub)), 
            u_triangle=(sin(degree), cos(degree), degree), 
            u_width=self.width, 
            u_round=self.round,
            **kwargs
            )
    
    def __copy__(self, start_pos=None, end_pos=None, width=None, texture=None, round=None,):
        return LineInfo(
                start_pos=choose_val(start_pos, self.start_pos[:]), 
                end_pos=choose_val(end_pos, self.end_pos[:]), 
                width=choose_val(width, self.width),
                round=choose_val(round, self.round), 
                texture=choose_val(texture, self.texture.__copy__()), 
            )


class RectInfo(WithTextureInfo):
    def __init__(self, rect_area, round=0.0, width=0.0, texture=None):
        super().__init__(texture)
        self.rect_area = rect_area
        self.round = round
        self.width = width

    def apply_uniform(self, model, **kwargs):
        super().apply_uniform(
            model,
            u_rect_area=self.rect_area,
            u_round=self.round,
            u_width=self.width,
            **kwargs
        )
    
    def __copy__(self, rect_area=None, round=None, width=None, texture=None,):
        return RectInfo(
            rect_area=choose_val(rect_area, self.rect_area[:]), 
            round=choose_val(round, self.round), 
            width=choose_val(width, self.width), 
            texture=choose_val(texture, self.texture.__copy__()), 
        )


class CircleInfo(WithTextureInfo):
    def __init__(self, pos, r=20, width=0, degree=(0, pi*2), round=0, texture=None):
        super().__init__(texture)
        self.pos = pos
        self.r = r
        self.width = width
        self.degree = degree
        self.round = round

    def apply_uniform(self, model, **kwargs):
        degree = self.degree
        if self.degree[1] < self.degree[0]:
            degree += degree[0], degree[1] + 3.1415926 * 2
            
        super().apply_uniform(
            model,
            u_pos=self.pos,
            u_r=self.r,
            u_width=self.width,
            u_degree=degree,
            u_round=self.round,
        )
    
    def __copy__(self, pos=None, r=None, width=None, degree=None, round=None, texture=None):
        return CircleInfo(
            pos=choose_val(pos, self.pos[:]),
            r=choose_val(r, self.r), 
            width=choose_val(width, self.width), 
            degree=choose_val(degree, self.degree[:]), 
            round=choose_val(round, self.round), 
            texture=choose_val(texture, self.texture.__copy__()), 
            )



