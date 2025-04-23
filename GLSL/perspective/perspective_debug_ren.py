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


def mix(a, b, k):
    return a + (b-a) * k

def mix_ft(t: tuple, f: float):
    return tuple(i*f for i in t)

def mix_tt(a: tuple, b: tuple):
    if len(a) == len(b):
        return tuple(a[i]*b[i] for i in range(len(a)))
    raise Exception(f"Tuple Length wrong: \na: {a}\nb: {b}")

def cost_tt(a: tuple, b: tuple):
    if len(a) == len(b):
        return tuple(a[i]-b[i] for i in range(len(a)))
    raise Exception(f"Tuple Length wrong: \na: {a}\nb: {b}")

def add_tt(a: tuple, b: tuple):
    if len(a) == len(b):
        return tuple(a[i]+b[i] for i in range(len(a)))
    raise Exception(f"Tuple Length wrong: \na: {a}\nb: {b}")

def t_int(t: tuple):
    return tuple(int(i) for i in t)

def trans_to_rect(t: tuple):
    return (t[0], t[2], t[1]-t[0], t[3]-t[2])



# Debug 用的 UI 控件
class DebugBarThumb(renpy.Displayable):
    def __init__(self):
        super().__init__()
        self.percent = 0.0
    
    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)
        rv.canvas().circle((255, 255, 255), (width/2, height/2), 10, 2)
        rv.canvas().circle((0, 0, 0, 100), (width/2, height/2), 8, 2)
        rv.canvas().circle((255, 255, 255, 100), (width/2, height/2), 6, 6)
        return rv


# Debug 用的 UI 控件
class DebugBarBase(renpy.Displayable):
    def __init__(self):
        super().__init__()
    
    def render(self, width, height, st, at):
        rv = renpy.Render(width, height)
        rv.canvas().line(
            color=(255, 255, 255), 
            start_pos=(height/2, height/2), 
            end_pos=(width-height/2, height/2), 
            width=5)
        rv.canvas().line(
            color=(50, 50, 50), 
            start_pos=(height/2 + 2, height/2), 
            end_pos=(width-height/2 - 2, height/2), 
            width=2)
        return rv


# Debug 用的 UI 控件
class DebugBar(renpy.Displayable):
    def __init__(self, name, cdd, get_val, set_val=None, val_range=(0.0, 1.0), default_val=None, hide_bar_value=False, api_val_parsing=None):
        super().__init__(cdd)
        self.name = Text(name, size=20)
        self.val = Text("", size=25)
        self.cdd = cdd
        self.get_val = get_val
        self.set_val = set_val
        self.range = val_range
        self.default = default_val if default_val is not None else get_val(self.cdd)
        self.pressing = False
        self.press_pos = (0, 0)
        self.width = 1920
        self.height = 0
        self.hide_bar_value = hide_bar_value
        self.api_val_parsing = api_val_parsing
        self.dynamic = True
        self.base = DebugBarBase()
        self.thumb = DebugBarThumb()

    def render(self, width, height, st, at):
        percent = (self.get_val(self.cdd) - self.range[0]) / (self.range[1] - self.range[0])
        percent = 1.0 if percent > 1 else percent
        percent = 0.0 if percent < 0 else percent

        self.width = width
        self.height = 30

        width = self.width
        height = self.height

        rv = renpy.Render(self.width, self.height)

        val = self.get_val(self.cdd)
        if isinstance(val, float):
            text = "%.4f" % val
        else:
            text = str(val)
        self.val.set_text(text)

        name_render = renpy.render(self.name, width, height, st, at)
        base_render = renpy.render(self.base, width, height, st, at)
        thumb_render = renpy.render(self.thumb, height, height, st, at)
        val_render = renpy.render(self.val, height, height, st, at)

        rv.blit(name_render, (0, 10-name_render.get_size()[1]))
        rv.blit(base_render, (0, 0))
        rv.blit(thumb_render, ((width - height) * percent, 0))
        rv.blit(val_render, (width, height-val_render.get_size()[1]))

        if self.dynamic:
            renpy.redraw(self, 0)

        return rv
    
    def event(self, ev, x, y, st):
        if self.set_val is None:
            return
        if ev.type == pygame.MOUSEBUTTONUP and ev.button == 3 and (0 < x < self.width and 0 < y < self.height):
            self.set_val(self.cdd, self.default)
            raise renpy.display.core.IgnoreEvent()

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and (0 < x < self.width and 0 < y < self.height):
            self.pressing = True

            percent = (x - self.height / 2) / (self.width - self.height)

            self.press_pos_x = renpy.get_mouse_pos()[0]
            self.old_percent = percent
            self.old_width = (self.width - self.height)

            percent = 1.0 if percent > 1 else percent
            percent = 0.0 if percent < 0 else percent
            self.set_val(self.cdd, int((self.range[0] + (self.range[1] - self.range[0]) * percent) * 1000) / 1000)
            renpy.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()
            
        if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1 and self.pressing:
            self.pressing = False
            renpy.redraw(self, 0)
            raise renpy.display.core.IgnoreEvent()

        if ev.type == pygame.MOUSEMOTION and self.pressing:
            
            slow = pygame.key.get_pressed()[pygame.K_LSHIFT]

            cost_x = (renpy.get_mouse_pos()[0] - self.press_pos_x) * (0.1 if slow else 1.0)
            percent = self.old_percent + (cost_x) / self.old_width

            percent = 1.0 if percent > 1 else percent
            percent = 0.0 if percent < 0 else percent
            self.set_val(self.cdd, int((self.range[0] + (self.range[1] - self.range[0]) * percent) * 1000) / 1000)
            renpy.redraw(self, 0)

            raise renpy.display.core.IgnoreEvent()

    @property
    def api_value(self):
        if self.hide_bar_value:
            return None
        elif self.api_val_parsing:
            val = eval(api_val_parsing, {"self": self.cdd})
        else:
            val = str(self.get_val(self.cdd))[:6]

        val = val[:6] if len(val) > 6 else val

        if self.api_value_text.text != val:
            self.api_value_text.set_text(val)
        
        return val


# 使用 Pygame 在 image 上显示出 center 和 area 位置的可视化组件
class PerspectivePreview(renpy.Displayable):
    def __init__(self, image, center, area, width=2, draw_center=True):
        super().__init__()
        self.image = renpy.displayable(image)
        self.center = center
        self.area = area
        self.width = width
        self.draw_center = draw_center
    
    def render(self, width, height, st, at):
        rend = renpy.render(self.image, width, height, st, at)

        size = rend.get_size()

        w, h = size

        rv = renpy.Render(*size)
        
        self.image.place(rv, 0, 0, *size, rend)

        center = mix(self.area[0], self.area[1], self.center[0]), mix(self.area[2], self.area[3], self.center[1])
        area = self.area

        canvas = rv.canvas()

        # 中心
        canvas.rect((255, 255, 255), trans_to_rect(mix_tt((w, w, h, h), area)), self.width)
        canvas.rect((255, 255, 255), (0, 0, w-self.width, h-self.width), self.width)

        if self.draw_center:
            canvas.line((255, 255, 255), mix_tt(center, size), mix_tt((area[0], area[2]), size), self.width)
            canvas.line((255, 255, 255), mix_tt(center, size), mix_tt((area[1], area[2]), size), self.width)
            canvas.line((255, 255, 255), mix_tt(center, size), mix_tt((area[0], area[3]), size), self.width)
            canvas.line((255, 255, 255), mix_tt(center, size), mix_tt((area[1], area[3]), size), self.width)

        # 左上
        canvas.line(
            (255, 255, 255), 
            mix_tt((area[0], area[2]), size), 
            add_tt(
                mix_tt((area[0], area[2]), size), 
                mix_ft(
                    cost_tt(
                        mix_tt((area[0], area[2]), size), 
                        mix_tt(center, size)
                        ), 
                    area[0]/(center[0]-area[0]))
                    ), 
            self.width)

        # 右上
        canvas.line(
            (255, 255, 255), 
            mix_tt((area[1], area[2]), size), 
            add_tt(
                mix_tt((area[1], area[2]), size), 
                mix_ft(
                    cost_tt(
                        mix_tt((area[1], area[2]), size), 
                        mix_tt(center, size)
                        ), 
                    area[1]/(area[1]-center[0]))
                    ), 
            self.width)

        # 左下
        canvas.line(
            (255, 255, 255), 
            mix_tt((area[0], area[3]), size), 
            add_tt(
                mix_tt((area[0], area[3]), size), 
                mix_ft(
                    cost_tt(
                        mix_tt((area[0], area[3]), size), 
                        mix_tt(center, size)
                        ), 
                    area[0]/(center[0]-area[0]))
                    ), 
            self.width)

        # 右下
        canvas.line(
            (255, 255, 255), 
            mix_tt((area[1], area[3]), size), 
            add_tt(
                mix_tt((area[1], area[3]), size), 
                mix_ft(
                    cost_tt(
                        mix_tt((area[1], area[3]), size), 
                        mix_tt(center, size)
                        ), 
                    area[1]/(area[1]-center[0]))
                    ), 
            self.width)

        # canvas.line((255, 255, 255), (0, 0), (int((self.center[0] + center[0])*10000), int((self.center[1] + center[1])*10000)), self.width)

        # print(area, center)
        # print(cost_tt((area[0], area[2]), center))

        return rv


# 根据子组件的属性来生成对应的 Bar 用于调试的组件
class PerspectiveValMonitor(renpy.Displayable):
    def __init__(self, cdd):
        super().__init__()
        self.cdd = cdd
        info = cdd.__dir__()
        self.enable_area = "area" in info
        self.enable_center = "center" in info
        self.enable_intensity = "intensity" in info
        # self.enable_debug = "enable_debug" in info
        # self.enable_draw_center = "draw_center" in info
        self.bar_bg = renpy.displayable("#0008")
        self.bar_area = (50, 50, 300, 50)
        self.bar = tuple()
        self.init_bar()
    
    def init_bar(self):
        bar = list()

        def get_set(name):
            def set_val(cdd, val):
                exec(f"cdd.{name} = val", {}, {"cdd": cdd, "val": val})
            return set_val
        
        def set_center(index):
            def set_val(cdd, val):
                cdd.center = (cdd.center[0] if index != 0 else val, cdd.center[1] if index != 1 else val)
                renpy.redraw(cdd, 0)
            return set_val

        def set_area(index):
            def set_val(cdd, val):
                cdd.area = tuple(cdd.area[i] if i != index else val for i in range(4))
                renpy.redraw(cdd, 0)
            return set_val
        
        if self.enable_center:
            bar.append(DebugBar("Center X", self.cdd, lambda cdd: cdd.center[0], set_center(0)))
            bar.append(DebugBar("Center Y", self.cdd, lambda cdd: cdd.center[1], set_center(1)))

        if self.enable_area:
            bar.append(DebugBar("Area X", self.cdd, lambda cdd: cdd.area[0], set_area(0)))
            bar.append(DebugBar("Area W", self.cdd, lambda cdd: cdd.area[1], set_area(1)))
            bar.append(DebugBar("Area Y", self.cdd, lambda cdd: cdd.area[2], set_area(2)))
            bar.append(DebugBar("Area H", self.cdd, lambda cdd: cdd.area[3], set_area(3)))

        if self.enable_intensity:
            bar.append(DebugBar("Intensity", self.cdd, lambda cdd: cdd.intensity, get_set("intensity"), val_range=(0.0, 1.2)))

        self.bar = tuple(bar)

    def render(self, w, h, st, at):
        rv = renpy.Render(w, h)
        son_rend = renpy.render(self.cdd, w, h, st, at)

        self.cdd.place(rv, 0, 0, w, h, son_rend)

        rv.blit(self.bar_bg.render(self.bar_area[2] + 100, self.bar_area[3] * len(self.bar), st, at), (self.bar_area[0]-20, self.bar_area[1]-20))

        ypos = self.bar_area[1]
        for bar in self.bar:
            bar_rend = renpy.render(bar, self.bar_area[2], self.bar_area[3], st, at)
            bar.place(rv, self.bar_area[0], ypos, self.bar_area[2], self.bar_area[3], bar_rend)
            ypos += self.bar_area[3]
        
        return rv
    
    def event(self, ev, x, y, st):
        self.cdd.event(ev, x, y, st)
        
        ypos = self.bar_area[1]
        
        for bar in self.bar:
            bar.event(ev, x - self.bar_area[0], y - ypos, st)
            ypos += self.bar_area[3]
        
        return

