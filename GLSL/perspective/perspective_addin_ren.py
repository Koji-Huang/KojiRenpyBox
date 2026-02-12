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

import pygame
from math import sin, cos


def mix(a, b, k):
    if 0 < k < 1:
        return a + (b-a) * k
    else:
        return a if k < 0 else b

def mix_tt(a: tuple, b: tuple):
    if len(a) == len(b):
        return tuple(a[i]*b[i] for i in range(len(a)))
    raise Exception(f"Tuple Length wrong: \na: {a}\nb: {b}")

def add_tt(a: tuple, b: tuple):
    if len(a) == len(b):
        return tuple(a[i]+b[i] for i in range(len(a)))
    raise Exception(f"Tuple Length wrong: \na: {a}\nb: {b}")

def mix_ft(t: tuple, f: float):
    return tuple(i*f for i in t)

def cost_tt(a: tuple, b: tuple):
    if len(a) == len(b):
        return tuple(a[i]-b[i] for i in range(len(a)))
    raise Exception(f"Tuple Length wrong: \na: {a}\nb: {b}")

# mode: 0(与其他): 加算, 1: 乘算, 2: 加上乘算结果, 3: 覆盖
def count_as_mode(a, b, mode):
    if mode == 1:
        return mix_tt(a, b)
    elif mode == 2:
        return add_tt(a, mix_tt(a, b))
    elif mode == 3:
        return b
    else:
        return add_tt(a, b)

def format_area(area):
    if isinstance(area[0], Iterable):
        if len(area) == 2:
            return tuple(area[int(i/2)] for i in range(4))
        elif len(area) == 4:
            return area
        else:
            raise Exception("Area format wrong:\ntuple[tuple[float, float], ...] -> len in (2, 4)\n", area)
    else:
        if len(area) == 4:
            return tuple((-area[i], area[i]) for i in range(4))
        elif len(area) == 8:
            return tuple((area[i*2], area[i*2+1]) for i in range(4))
        else:
            raise Exception("Area format wrong:\ntuple[float, ...] -> len in (4, 8)\n", area)

def format_center(center):
    if isinstance(center[0], Iterable):
        return center
    elif isinstance(center[0], float):
        if len(center) == 2:
            return tuple((-i, i) for i in center)
        elif len(center == 4):
            return tuple((center[i*2], center[i*2]+1) for i in range(2))
        else:
            raise Exception("CenterValueFormatWrong\ntuple[float, ...] len in [2, 4]\n", center)
    else:
        raise Exception("CenterValueFormatWrong\ntuple[tuple[float, float]] -> len 2 | tuple[float, ...] len in [2, 4]\n", center)


class BaseAddin:
    def __init__(self, ):
        pass
    
    @abstractmethod
    def event(self, obj, ev, x, y, st):
        pass

    @abstractmethod
    def render(self, obj, w, h, st, at):
        pass



# 重置参数插件
class ResetArgAddin(BaseAddin):
    def __init__(self):
        super().__init__()

    def event(self, obj, ev, x, y, st):
        pass

    def render(self, obj, w, h, st, at):
        obj.reset_arg()


# 根据鼠标位置形变 Center 插件
class CenterMouseTrackAddin(BaseAddin):
    def __init__(self, center=(1.0, 1.0), catch_fullscreen=False, mode=2):
        super().__init__()
        self.center = format_center(center)
        self.size = None
        self.pos = None
        self.mode = mode
        self.catch_fullscreen = catch_fullscreen

    def event(self, obj, ev, x, y, st):
        if ev.type != pygame.MOUSEMOTION:
            return
        if self.catch_fullscreen:
            self.pos = renpy.get_mouse_pos()
        else:
            self.pos = (x, y)
    
    def render(self, obj, w, h, st, at):
        if self.catch_fullscreen:
            self.size = (config.screen_width, config.screen_height)
        else:
            self.size = (w, h)

        if self.pos is not None:
            center = obj.center
            val = mix(self.center[0][0], self.center[0][1], self.pos[0] / self.size[0]), mix(self.center[1][0], self.center[1][1], self.pos[1] / self.size[1])

            obj.center = count_as_mode(center, val, self.mode)
                    

# 根据鼠标位置形变 Area 插件
class AreaMouseTrackAddin(BaseAddin):
    def __init__(self, area=(1.0, 1.0, 1.0, 1.0), catch_fullscreen=False, mode=2):
        super().__init__()
        self.area = format_area(area)
        self.size = None
        self.pos = None
        self.mode = 0
        self.catch_fullscreen = catch_fullscreen

    def event(self, obj, ev, x, y, st):
        if ev.type != pygame.MOUSEMOTION:
            return
        if self.catch_fullscreen:
            self.pos = renpy.get_mouse_pos()
        else:
            self.pos = (x, y)
    
    def render(self, obj, w, h, st, at):
        if self.catch_fullscreen:
            self.size = (1920, 1080)
        else:
            self.size = (w, h)
        
        if self.pos is None:
            return

        area = obj.area
        
        val = tuple(mix(self.area[i][0], self.area[i][1], self.pos[int(i/2)] / self.size[int(i/2)]) for i in range(4))

        obj.area = count_as_mode(area, val, self.mode)


# 根据鼠标滚轮形变 Intensity 插件
class IntensityAddin(BaseAddin):
    def __init__(self, intensity = 0.1, count=10, limit=(0.1, 1.2), speed=10, mode=3):
        super().__init__()
        self.intensity = intensity
        self.count = count
        self.mode = mode
        self.limit = limit
        self.speed = speed
        self.now_scale = self.count * self.intensity
        self.last_st = None
    
    def event(self, obj, ev, x, y, st):
        if ev.type == pygame.MOUSEBUTTONDOWN: 
            if ev.button == 4:
                self.count += self.is_in_range(1)
            if ev.button == 5:
                self.count -= self.is_in_range(-1)
    
    def render(self, obj, w, h, st, at):
        if self.last_st is None:
            self.last_st = st - 0.01

        target = self.count * self.intensity

        if self.is_in_range() is False:
            target = mix(*self.limit, target > self.limit[0])

        self.now_scale = mix(self.now_scale, target, self.speed*(st-self.last_st))

        self.last_st = st

        if self.mode == 1:
            obj.intensity = obj.intensity + self.now_scale
        elif self.mode == 2:
            obj.intensity += obj.intensity + self.now_scale
        elif self.mode == 3:
            obj.intensity = self.now_scale
        else:
            obj.intensity += self.now_scale
        
        # print(obj.intensity)
    
    def is_in_range(self, addin=0):
        target = (self.count + addin) * self.intensity
        return (self.limit[0] <= target <= self.limit[1])


# 根据鼠标滚轮形变 Area 插件
class ScaleAreaAddin(BaseAddin):
    def __init__(self, area=0.1, count=0, limit_count = (-10, 2), speed=10, mode=0):
        super().__init__()
        self.count = count
        self.speed = speed

        if isinstance(area, Iterable):
            if len(area) == 2:
                self.area = (-area[0], area[0], -area[1], area[1])
            elif len(area) == 4:
                self.area = area
            else:
                raise Exception("PerScale format wrong:\ntuple[float, float], tuple[float, float, float, float]\n", area)
        else:
            self.area = tuple(area*((i%2)-0.5)*2 for i in range(4))

        self.limit_count = limit_count
        self.now_count = 0.0
        self.mode = mode
        self.last_st = None

    def event(self, obj, ev, x, y, st):
        if ev.type == pygame.MOUSEBUTTONDOWN: 
            if ev.button == 4:
                self.count += self.is_in_range(1)
            if ev.button == 5:
                self.count -= self.is_in_range(-1)
    
    def render(self, obj, w, h, st, at):
        if self.last_st is None:
            self.last_st = st - 0.01

        self.now_count = mix(self.now_count, self.count, self.speed*(st - self.last_st))

        self.last_st = st

        offset = (
            (obj.area[0] - obj.area[1]) * self.area[0] / 2, 
            (obj.area[0] - obj.area[1]) * self.area[1] / 2, 
            (obj.area[2] - obj.area[3]) * self.area[2] / 2, 
            (obj.area[2] - obj.area[3]) * self.area[3] / 2
            )
        
        scaled = mix_ft(offset, self.now_count)

        obj.area = count_as_mode(obj.area, scaled, self.mode)

    def is_in_range(self, addin=0):
        target = (self.count + addin)
        return (self.limit_count[0] <= target <= self.limit_count[1])


# 参数限制插件 ( Not Debugged )
class ArgsLimitAddin(BaseAddin):
    def __init__(self, area_check=(1.0, 1.0, 1.0, 1.0), center_check=((0.0, 1.0), (0.0, 1.0)), intensity_range=(0.0, 1.2)):
        super().__init__()
        self.area_check = format_area(area_check) if bool(area_check) else False
        self.center_check = format_center(center_check) if bool(center_check) else False
        self.intensity_check = intensity_check
    
    def event(self, *args, **kwargs):
        pass

    def render(self, obj, w, h, st, at):
        if self.area_check:
            area = list()
            for i in range(4):
                if self.area_check[i][0] < obj.area[i] < self.area_check[i][1]:
                    area.append(obj.area[i])
                else:
                    area.append(self.area_check[i][1] if obj.area[i] > self.area_check[i][0] else self.area_check[i][0])
            obj.area = tuple(area)
            
        if self.center_check:
            center = list()
            for i in range(2):
                if self.center_check[i][0] < obj.center[i] < self.center_check[i][1]:
                    center.append(obj.center[i])
                else:
                    center.append(self.center_check[i][1] if obj.center[i] > self.center_check[i][0] else self.center_check[i][0])
            obj.center = tuple(center)

        if self.intensity_check:
            if self.intensity_check[0] < obj.intensity < self.intensity_check[1]:
                intensity.append(obj.intensity)
            else:
                intensity.append(self.intensity_check[1] if obj.intensity > self.intensity_check[0] else self.intensity_check[0])

            obj.intensity = intensity

# 弃用项, 原本是将鼠标位置 Area 形变和鼠标滚轮形变组合到一起的东西, 但现在两个插件独立起来也是可以用的了
# class AreaMouseTrackScaleAddin:
#     def __init__(self, area_shape=None, limit=(-0.5, 0.5, -0.5, 0.5), catch_fullscreen=False, area=-0.05):
#         self.area = limit
#         self.shape = area_shape
#         self.size = None
#         self.pos = None
#         self.catch_fullscreen = catch_fullscreen

#         self.count = 0
#         self.area = area
#         self.now_scale = 0.0

#     def event(self, obj, ev, x, y, st):
#         if ev.type == pygame.MOUSEBUTTONDOWN: 
#             if ev.button == 4:
#                 self.count += 1
#             if ev.button == 5:
#                 self.count -= 1

#         if ev.type != pygame.MOUSEMOTION:
#             return
#         if self.catch_fullscreen:
#             self.pos = renpy.get_mouse_pos()
#         else:
#             self.pos = (x, y)
        
    
#     def render(self, obj, w, h, st, at):
#         if self.catch_fullscreen:
#             self.size = (1920, 1080)
#         else:
#             self.size = (w, h)
        
#         if self.pos is None:
#             return

#         shape = obj.area if self.shape is None else self.shape
        
#         offset_x = mix(self.area[0], self.area[1], self.pos[0] / self.size[0])
#         offset_y = mix(self.area[2], self.area[3], self.pos[1] / self.size[1])


#         self.now_scale = mix(self.now_scale, self.count * self.area, 0.1)
#         offset = ((obj.area[0] - obj.area[1]) * self.now_scale / 2, (obj.area[2] - obj.area[3]) * self.now_scale / 2)
        
#         obj.area = (offset_x + obj.area[0] + offset[0], offset_x + obj.area[1] - offset[0], offset_y + obj.area[2] + offset[1], offset_y + obj.area[3] - offset[1])
